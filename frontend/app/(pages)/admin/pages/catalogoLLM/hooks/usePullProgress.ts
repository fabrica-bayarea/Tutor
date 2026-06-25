"use client";

import { useEffect, useRef, useState } from "react";
import { obterStatusPull } from "@/app/services/service_llm";
import { PullProgress } from "@/app/types";

// Fases derivadas do `status` textual do backend (espelha as constantes de
// service_llm.py). Qualquer status não-terminal é tratado como "baixando".
export type PullPhase = "baixando" | "concluido" | "erro";

const STATUS_CONCLUIDO = "concluido";
const STATUS_ERRO = new Set(["erro", "modelo_nao_encontrado"]);

// Após esta quantidade de falhas consecutivas de polling, o hook desiste — evita
// martelar o servidor para sempre (ex.: modelo removido durante o download).
const MAX_FALHAS_CONSECUTIVAS = 5;

function derivarFase(progresso: PullProgress): PullPhase {
    if (STATUS_ERRO.has(progresso.status)) return "erro";
    if (progresso.status === STATUS_CONCLUIDO || progresso.percent >= 100) {
        return "concluido";
    }
    return "baixando";
}

type UsePullProgressOptions = {
    /** Quando false, o polling nem inicia (ex.: modelo já ativo). Padrão: true. */
    enabled?: boolean;
    /** Intervalo entre consultas, em ms. Padrão: 2000 (regra da US). */
    intervalMs?: number;
    /** Chamado uma vez quando o download conclui (100% / "concluido"). */
    onConcluido?: () => void;
    /** Chamado uma vez quando o download falha. */
    onErro?: (status: string) => void;
};

type UsePullProgressResult = {
    progresso: PullProgress | null;
    fase: PullPhase | null;
};

/**
 * Acompanha o progresso do download de um modelo por polling, com ciclo de vida
 * à prova de vazamentos:
 *
 * - usa `setTimeout` recursivo (não `setInterval`): só agenda o próximo tick após
 *   a resposta chegar, sem empilhar requisições em rede lenta;
 * - cancela a requisição em voo (`AbortController`) e ignora respostas tardias
 *   (flag `ativo`) no cleanup, nunca chamando `setState` após o unmount;
 * - encerra sozinho ao atingir um estado terminal (concluído/erro) ou após
 *   falhas consecutivas demais.
 *
 * Faz uma leitura imediata no mount, o que classifica o card (instalado x
 * baixando) sem esperar o primeiro intervalo — cobrindo inclusive o refresh da
 * página durante um download.
 */
export function usePullProgress(
    modelId: string,
    options: UsePullProgressOptions = {}
): UsePullProgressResult {
    const { enabled = true, intervalMs = 2000, onConcluido, onErro } = options;

    const [progresso, setProgresso] = useState<PullProgress | null>(null);
    const [fase, setFase] = useState<PullPhase | null>(null);

    // Callbacks em refs: o pai costuma recriá-las a cada render, e sem isto o
    // efeito reiniciaria — zerando o polling — toda vez que ele renderizasse.
    const onConcluidoRef = useRef(onConcluido);
    const onErroRef = useRef(onErro);
    useEffect(() => {
        onConcluidoRef.current = onConcluido;
        onErroRef.current = onErro;
    });

    useEffect(() => {
        if (!enabled || !modelId) return;

        let ativo = true;
        let timer: ReturnType<typeof setTimeout> | null = null;
        let falhas = 0;
        const controller = new AbortController();

        const agendarProximo = () => {
            timer = setTimeout(consultar, intervalMs);
        };

        const consultar = async () => {
            const resultado = await obterStatusPull(modelId, controller.signal);

            // Desmontou (ou o efeito foi recriado) durante o await: não mexe mais
            // em estado nem agenda novos ticks.
            if (!ativo) return;

            if (!resultado) {
                falhas += 1;
                if (falhas >= MAX_FALHAS_CONSECUTIVAS) {
                    setFase("erro");
                    onErroRef.current?.("erro");
                    return;
                }
                agendarProximo();
                return;
            }

            falhas = 0;
            setProgresso(resultado);
            const faseAtual = derivarFase(resultado);
            setFase(faseAtual);

            if (faseAtual === "concluido") {
                onConcluidoRef.current?.();
                return;
            }
            if (faseAtual === "erro") {
                onErroRef.current?.(resultado.status);
                return;
            }

            agendarProximo();
        };

        // Leitura imediata no mount.
        consultar();

        return () => {
            ativo = false;
            controller.abort();
            if (timer) clearTimeout(timer);
        };
    }, [modelId, enabled, intervalMs]);

    return { progresso, fase };
}
