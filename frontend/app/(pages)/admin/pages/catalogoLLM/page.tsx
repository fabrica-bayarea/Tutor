"use client";

import { useCallback, useEffect, useState } from "react";
import { Plus, Power } from "lucide-react";
import Button from "@/app/components/Button/Button";
import Modal from "@/app/components/Modal/Modal";
import { useToast } from "@/contexts/ToastContext";
import { InterfaceLLM } from "@/app/types";
import { listarModelos, ativarModelo } from "@/app/services/service_llm";
import CardModeloLLM from "./components/CardModeloLLM/CardModeloLLM";
import ModalAdicionarLLM from "./components/ModalAdicionarLLM/ModalAdicionarLLM";
import styles from "./page.module.css";

export default function CatalogoLLM() {
    const { addToast } = useToast();
    const [modelos, setModelos] = useState<InterfaceLLM[]>([]);
    const [carregando, setCarregando] = useState(true);
    const [modalAddAberto, setModalAddAberto] = useState(false);
    const [modeloParaAtivar, setModeloParaAtivar] = useState<InterfaceLLM | null>(null);
    const [ativando, setAtivando] = useState(false);

    const carregar = useCallback(async () => {
        const lista = await listarModelos();
        setModelos(lista);
        setCarregando(false);
    }, []);

    useEffect(() => {
        carregar();
    }, [carregar]);

    const modeloAtivo = modelos.find((m) => m.status === "ativada") ?? null;

    async function confirmarAtivacao() {
        if (!modeloParaAtivar) return;

        setAtivando(true);
        const resultado = await ativarModelo(modeloParaAtivar.id);
        setAtivando(false);

        if (resultado.ok) {
            addToast(`Modelo ${modeloParaAtivar.nome} ativado com sucesso.`, "success");
            setModeloParaAtivar(null);
            carregar();
            return;
        }

        addToast(resultado.message, "error");
        setModeloParaAtivar(null);
    }

    return (
        <div className={styles.pagina}>
            <div className={styles.topo}>
                <div>
                    <h2 className={styles.titulo}>Catálogo de modelos de IA</h2>
                    <p className={styles.subtitulo}>
                        Adicione, baixe e ative os modelos de linguagem usados pela
                        plataforma. Apenas um modelo fica ativo por vez.
                    </p>
                </div>
                <Button
                    style="filled"
                    action="primary"
                    icon={<Plus size={16} />}
                    label="Adicionar LLM"
                    onClick={() => setModalAddAberto(true)}
                />
            </div>

            <div className={styles.lista}>
                {carregando ? (
                    <p className={styles.estado}>Carregando modelos...</p>
                ) : modelos.length === 0 ? (
                    <p className={styles.estado}>
                        Nenhum modelo cadastrado. Use <strong>Adicionar LLM</strong> para
                        baixar o primeiro.
                    </p>
                ) : (
                    modelos.map((modelo) => (
                        <CardModeloLLM
                            key={modelo.id}
                            modelo={modelo}
                            onAtivar={setModeloParaAtivar}
                        />
                    ))
                )}
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
                icon={<Power size={20} color="#0d9488" />}
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
                            action="primary"
                            label={
                                ativando
                                    ? "Ativando..."
                                    : `Ativar ${modeloParaAtivar?.nome ?? ""}`
                            }
                            onClick={confirmarAtivacao}
                            isDisabled={ativando}
                        />
                    </>
                }
            >
                {modeloParaAtivar &&
                    (modeloAtivo ? (
                        <p className={styles.modalTexto}>
                            O modelo <strong>{modeloAtivo.nome}</strong> deixará de atender
                            novas mensagens e o <strong>{modeloParaAtivar.nome}</strong>{" "}
                            passará a ser o modelo ativo. As conversas em andamento seguem
                            normalmente com o modelo atual.
                        </p>
                    ) : (
                        <p className={styles.modalTexto}>
                            O <strong>{modeloParaAtivar.nome}</strong> passará a ser o modelo
                            ativo da plataforma e responderá a todas as novas mensagens.
                        </p>
                    ))}
            </Modal>
        </div>
    );
}
