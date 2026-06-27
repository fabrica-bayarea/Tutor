"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Plus, Info, Settings, Zap, Download, CircleCheck, AlertTriangle } from "lucide-react";
import Button from "@/app/components/Button/Button";
import Modal from "@/app/components/Modal/Modal";
import ProgressBar from "@/app/components/ProgressBar/ProgressBar";
import { useToast } from "@/contexts/ToastContext";
import { InterfaceLLM } from "@/app/types";
import { listarModelos, ativarModelo, adicionarModelo } from "@/app/services/service_llm";
import { CATALOGO_LLM, LinhaModelo, MSG } from "./constants";
import { usePullProgressMulti } from "./hooks/usePullProgressMulti";
import ModalAdicionarLLM from "./components/ModalAdicionarLLM/ModalAdicionarLLM";
import styles from "./page.module.css";

export default function CatalogoLLM() {
    const { addToast } = useToast();
    const [modelos, setModelos] = useState<InterfaceLLM[]>([]);
    const [carregando, setCarregando] = useState(true);
    const [modalAddAberto, setModalAddAberto] = useState(false);
    const [modeloParaAtivar, setModeloParaAtivar] = useState<LinhaModelo | null>(null);
    const [ativando, setAtivando] = useState(false);
    const [iniciandoDownload, setIniciandoDownload] = useState<Set<string>>(new Set());

    const carregar = useCallback(async () => {
        const lista = await listarModelos();
        if (lista === null) {
            addToast(MSG.listaErro, "error");
            setModelos([]);
        } else {
            setModelos(lista);
        }
        setCarregando(false);
    }, [addToast]);

    useEffect(() => {
        carregar();
    }, [carregar]);

    // Junta o catálogo estático com o que está cadastrado na API (cruzando por nome).
    const linhas: LinhaModelo[] = useMemo(() => {
        const porNome = new Map(modelos.map((m) => [m.nome, m]));

        const doCatalogo: LinhaModelo[] = CATALOGO_LLM.map((c) => {
            const api = porNome.get(c.nome);
            return {
                nome: c.nome,
                descricao: c.descricao,
                tamanho: c.tamanho,
                id: api?.id ?? null,
                cadastrado: !!api,
                ativo: api?.status === "ativada",
            };
        });

        // Modelos adicionados pelo admin que não estão no catálogo curado.
        const nomesCatalogo = new Set(CATALOGO_LLM.map((c) => c.nome));
        const extras: LinhaModelo[] = modelos
            .filter((m) => !nomesCatalogo.has(m.nome))
            .map((m) => ({
                nome: m.nome,
                descricao: "Modelo personalizado",
                tamanho: "—",
                id: m.id,
                cadastrado: true,
                ativo: m.status === "ativada",
            }));

        return [...doCatalogo, ...extras];
    }, [modelos]);

    // Só os cadastrados e não-ativos podem estar baixando — são os observados pelo polling.
    const idsObservados = useMemo(
        () => linhas.filter((l) => l.cadastrado && !l.ativo && l.id).map((l) => l.id as string),
        [linhas]
    );
    const progresso = usePullProgressMulti(idsObservados);

    // Avisa (uma vez) quando um download falha — toast do protótipo (US-38.5).
    const errosNotificados = useRef<Set<string>>(new Set());
    useEffect(() => {
        linhas.forEach((linha) => {
            if (!linha.id) return;
            const fase = progresso[linha.id]?.fase;
            if (fase === "erro" && !errosNotificados.current.has(linha.id)) {
                errosNotificados.current.add(linha.id);
                addToast(MSG.falhaDownload(linha.nome), "error");
            } else if (fase === "baixando" && errosNotificados.current.has(linha.id)) {
                errosNotificados.current.delete(linha.id);
            }
        });
    }, [progresso, linhas, addToast]);

    const modeloAtivo = linhas.find((l) => l.ativo) ?? null;

    async function handleBaixar(linha: LinhaModelo) {
        // "Baixar" cadastra o modelo e dispara o pull no Ollama (POST /llm).
        setIniciandoDownload((s) => new Set(s).add(linha.nome));
        const resultado = await adicionarModelo(linha.nome);
        setIniciandoDownload((s) => {
            const novo = new Set(s);
            novo.delete(linha.nome);
            return novo;
        });

        if (resultado.ok) {
            addToast(MSG.downloadIniciado(linha.nome), "success");
            carregar();
            return;
        }
        addToast(
            resultado.status === 503 ? MSG.ollamaIndisponivel : MSG.falhaDownload(linha.nome),
            "error"
        );
    }

    async function confirmarAtivacao() {
        if (!modeloParaAtivar?.id) return;

        setAtivando(true);
        const resultado = await ativarModelo(modeloParaAtivar.id);
        setAtivando(false);

        if (resultado.ok) {
            addToast(MSG.ativadoSucesso(modeloParaAtivar.nome), "success");
            setModeloParaAtivar(null);
            carregar();
            return;
        }
        addToast(resultado.message, "error");
        setModeloParaAtivar(null);
    }

    function faseDe(linha: LinhaModelo) {
        return linha.id ? progresso[linha.id]?.fase : undefined;
    }

    function renderDescricao(linha: LinhaModelo) {
        const fase = faseDe(linha);
        if (linha.cadastrado && fase === "baixando") {
            const percent = (linha.id ? progresso[linha.id]?.progresso.percent : 0) ?? 0;
            return (
                <div className={styles.descDownload}>
                    <span>{linha.descricao}</span>
                    <ProgressBar value={percent} color="#ea580c" />
                    <span className={styles.percent}>Baixando... {percent}%</span>
                </div>
            );
        }
        return linha.descricao;
    }

    function renderStatus(linha: LinhaModelo) {
        if (linha.ativo) {
            return <span className={`${styles.badge} ${styles.badgeAtivo}`}>Ativo</span>;
        }
        const fase = faseDe(linha);
        if (linha.cadastrado && fase === "erro") {
            return <span className={`${styles.badge} ${styles.badgeErro}`}>Erro</span>;
        }
        if (linha.cadastrado && fase === "concluido") {
            return <span className={`${styles.badge} ${styles.badgeInstalado}`}>Instalado</span>;
        }
        return <span className={`${styles.badge} ${styles.badgeDisponivel}`}>Fazer Download</span>;
    }

    function renderAcao(linha: LinhaModelo) {
        if (linha.ativo) {
            return (
                <span className={styles.modeloAtivo}>
                    <CircleCheck size={16} /> Modelo ativo
                </span>
            );
        }

        const fase = faseDe(linha);

        if (linha.cadastrado && fase === "baixando") {
            // Durante o download, o progresso é exibido na coluna "Descrição".
            return null;
        }

        if (linha.cadastrado && fase === "concluido") {
            return (
                <Button
                    style="filled"
                    action="primary"
                    icon={<Zap size={16} />}
                    label="Ativar"
                    onClick={() => setModeloParaAtivar(linha)}
                />
            );
        }

        if (linha.cadastrado && fase === "erro") {
            return (
                <span className={styles.erroAcao}>
                    <AlertTriangle size={15} /> Falha no download
                </span>
            );
        }

        const iniciando = iniciandoDownload.has(linha.nome);
        return (
            <Button
                style="ghost"
                icon={<Download size={16} />}
                label={iniciando ? "Iniciando..." : "Baixar"}
                isDisabled={iniciando}
                onClick={() => handleBaixar(linha)}
                className={styles.btnBaixar}
            />
        );
    }

    return (
        <div className={styles.pagina}>
            <div className={styles.topo}>
                <Button
                    style="filled"
                    action="primary"
                    icon={<Plus size={16} />}
                    label="Adicionar LLM"
                    onClick={() => setModalAddAberto(true)}
                />
            </div>

            <div className={styles.tabelaWrapper}>
                <table className={styles.tabela}>
                    <thead>
                        <tr>
                            <th>Modelo</th>
                            <th>Descrição</th>
                            <th>Tamanho</th>
                            <th>Status</th>
                            <th className={styles.thAcoes}>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {carregando ? (
                            <tr>
                                <td colSpan={5} className={styles.estado}>Carregando modelos...</td>
                            </tr>
                        ) : linhas.length === 0 ? (
                            <tr>
                                <td colSpan={5} className={styles.estado}>Nenhum modelo disponível.</td>
                            </tr>
                        ) : (
                            linhas.map((linha) => (
                                <tr key={linha.nome} className={linha.ativo ? styles.linhaAtiva : undefined}>
                                    <td data-label="Modelo">
                                        <div className={styles.celModelo}>
                                            <span
                                                className={`${styles.engrenagem} ${linha.ativo ? styles.engrenagemAtiva : ""}`}
                                            >
                                                <Settings size={16} />
                                            </span>
                                            <span className={styles.nomeModelo}>{linha.nome}</span>
                                        </div>
                                    </td>
                                    <td data-label="Descrição" className={styles.celDescricao}>
                                        {renderDescricao(linha)}
                                    </td>
                                    <td data-label="Tamanho" className={styles.celTamanho}>
                                        {linha.tamanho}
                                    </td>
                                    <td data-label="Status" className={styles.celStatus}>
                                        {renderStatus(linha)}
                                    </td>
                                    <td className={styles.celAcao}>{renderAcao(linha)}</td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            <ModalAdicionarLLM
                open={modalAddAberto}
                onClose={() => setModalAddAberto(false)}
                onAdicionado={() => carregar()}
            />

            <Modal
                open={modeloParaAtivar !== null}
                onClose={() => {
                    if (!ativando) setModeloParaAtivar(null);
                }}
                title={modeloParaAtivar ? `Ativar o modelo ${modeloParaAtivar.nome}?` : ""}
                icon={<Info size={20} color="#2563eb" />}
                accentColor="#0d9488"
                showCloseButton
                closeOnBackdrop={!ativando}
                closeOnEsc={!ativando}
                footer={
                    <>
                        <Button
                            style="ghost"
                            label="Cancelar"
                            onClick={() => setModeloParaAtivar(null)}
                            isDisabled={ativando}
                        />
                        <Button
                            style="filled"
                            label={ativando ? "Ativando..." : `Ativar ${modeloParaAtivar?.nome ?? ""}`}
                            onClick={confirmarAtivacao}
                            isDisabled={ativando}
                            className={styles.btnAtivar}
                        />
                    </>
                }
            >
                {modeloParaAtivar &&
                    (modeloAtivo ? (
                        <p className={styles.modalTexto}>
                            O modelo <strong>{modeloAtivo.nome}</strong> deixará de atender novas
                            mensagens e o <strong>{modeloParaAtivar.nome}</strong> passará a ser o
                            modelo ativo. As conversas em andamento seguem normalmente com o modelo
                            atual.
                        </p>
                    ) : (
                        <p className={styles.modalTexto}>
                            O <strong>{modeloParaAtivar.nome}</strong> passará a ser o modelo ativo da
                            plataforma e responderá a todas as novas mensagens.
                        </p>
                    ))}
            </Modal>
        </div>
    );
}
