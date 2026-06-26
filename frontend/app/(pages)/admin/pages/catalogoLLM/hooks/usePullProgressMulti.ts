"use client";

import { useEffect, useState } from "react";
import { obterStatusPull } from "@/app/services/service_llm";
import { PullProgress } from "@/app/types";

// Fases derivadas do `status` textual do backend (espelha service_llm.py).
export type PullPhase = "baixando" | "concluido" | "erro";

const STATUS_CONCLUIDO = "concluido";
const STATUS_ERRO = new Set(["erro", "modelo_nao_encontrado"]);

export type ProgressoModelo = { progresso: PullProgress; fase: PullPhase };

function derivarFase(p: PullProgress): PullPhase {
    if (STATUS_ERRO.has(p.status)) return "erro";
    if (p.status === STATUS_CONCLUIDO || p.percent >= 100) return "concluido";
    return "baixando";
}

/**
 * Acompanha o download de vários modelos ao mesmo tempo (um por linha da tabela),
 * retornando um mapa `id -> { progresso, fase }`.
 *
 * Ciclo de vida à prova de vazamentos:
 * - faz uma leitura inicial de todos os ids e mantém o polling (`setTimeout`
 *   recursivo) enquanto algum estiver baixando; encerra quando todos chegam a um
 *   estado terminal (concluído/erro);
 * - cancela as requisições em voo (`AbortController`) e ignora respostas tardias
 *   (flag `ativo`) ao desmontar ou quando a lista de ids muda.
 *
 * A `idsKey` ordenada evita reiniciar o efeito por mera reordenação da lista.
 */
export function usePullProgressMulti(
    ids: string[],
    intervalMs = 2000
): Record<string, ProgressoModelo> {
    const [mapa, setMapa] = useState<Record<string, ProgressoModelo>>({});
    const idsKey = [...ids].sort().join(",");

    useEffect(() => {
        const idsAtuais = idsKey ? idsKey.split(",") : [];
        if (idsAtuais.length === 0) {
            setMapa({});
            return;
        }

        let ativo = true;
        let timer: ReturnType<typeof setTimeout> | null = null;
        const controller = new AbortController();

        const consultar = async () => {
            const pares = await Promise.all(
                idsAtuais.map(
                    async (id) =>
                        [id, await obterStatusPull(id, controller.signal)] as const
                )
            );
            if (!ativo) return;

            setMapa((prev) => {
                const novo = { ...prev };
                for (const [id, p] of pares) {
                    if (p) novo[id] = { progresso: p, fase: derivarFase(p) };
                }
                return novo;
            });

            const algumBaixando = pares.some(
                ([, p]) => p !== null && derivarFase(p) === "baixando"
            );
            if (algumBaixando) timer = setTimeout(consultar, intervalMs);
        };

        consultar();

        return () => {
            ativo = false;
            controller.abort();
            if (timer) clearTimeout(timer);
        };
    }, [idsKey, intervalMs]);

    return mapa;
}
