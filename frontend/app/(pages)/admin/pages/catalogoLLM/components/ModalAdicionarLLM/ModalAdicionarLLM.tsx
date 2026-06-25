"use client";

import { useState } from "react";
import { Download } from "lucide-react";
import Modal from "@/app/components/Modal/Modal";
import Button from "@/app/components/Button/Button";
import Input from "@/app/components/Input/Input";
import { useToast } from "@/contexts/ToastContext";
import { adicionarModelo } from "@/app/services/service_llm";
import { InterfaceLLM } from "@/app/types";
import styles from "./ModalAdicionarLLM.module.css";

type ModalAdicionarLLMProps = {
    open: boolean;
    onClose: () => void;
    onAdicionado: (modelo: InterfaceLLM) => void;
};

export default function ModalAdicionarLLM({
    open,
    onClose,
    onAdicionado,
}: ModalAdicionarLLMProps) {
    const { addToast } = useToast();
    const [nome, setNome] = useState("");
    const [erro, setErro] = useState("");
    const [enviando, setEnviando] = useState(false);

    function fechar() {
        if (enviando) return;
        setNome("");
        setErro("");
        onClose();
    }

    async function handleSubmit() {
        if (enviando) return;

        const valor = nome.trim();
        if (!valor) {
            setErro("Informe o nome do modelo.");
            return;
        }

        setErro("");
        setEnviando(true);
        const resultado = await adicionarModelo(valor);
        setEnviando(false);

        if (resultado.ok) {
            addToast(
                `Modelo ${resultado.modelo.nome} adicionado. O download foi iniciado.`,
                "success"
            );
            setNome("");
            onAdicionado(resultado.modelo);
            onClose();
            return;
        }

        // O backend já devolve mensagens claras (404 = inexistente no Ollama,
        // 409 = duplicado, 503 = Ollama fora). Exibimos no próprio modal.
        setErro(resultado.message || "Não foi possível adicionar o modelo.");
    }

    return (
        <Modal
            open={open}
            onClose={fechar}
            title="Adicionar modelo de IA"
            icon={<Download size={20} color="#0d9488" />}
            accentColor="#0d9488"
            showCloseButton
            closeOnBackdrop={!enviando}
            closeOnEsc={!enviando}
            footer={
                <>
                    <Button
                        style="ghost"
                        label="Cancelar"
                        onClick={fechar}
                        isDisabled={enviando}
                    />
                    <Button
                        style="filled"
                        action="primary"
                        label={enviando ? "Adicionando..." : "Adicionar"}
                        onClick={handleSubmit}
                        isDisabled={enviando}
                    />
                </>
            }
        >
            <p className={styles.descricao}>
                O modelo será baixado do Ollama e ficará disponível para ativação. O
                download começa assim que você confirmar e pode levar alguns minutos.
            </p>
            <Input
                label="Nome do modelo no Ollama"
                placeholder="ex.: llama3, mistral, phi3"
                value={nome}
                onChange={(e) => {
                    setNome(e.target.value);
                    if (erro) setErro("");
                }}
                onKeyDown={(e) => {
                    if (e.key === "Enter") handleSubmit();
                }}
                error={erro || undefined}
                helperText="Informe exatamente como aparece na biblioteca do Ollama."
                disabled={enviando}
                maxLength={64}
                autoFocus
            />
        </Modal>
    );
}
