"use client"

import { useEffect, useRef, useState } from "react";
import Header from "./components/Header/Header"
import MessageField, { MessageFieldRef } from "./components/MessageField/MessageField"
import TextArea from "./components/TextArea/TextArea"
import NoMessageField from "./components/NoMessageField/NoMessageField";

import { promptDeep, promptExam, promptQuestion, promptSummarize } from "./utils/prompts";
import ErrorField from "./components/ErrorField/ErrorField";
import { useData } from "@/utils/data";
import { useAuth } from "@/utils/auth";
import styles from "./page.module.css"
import socket from "../../../libs/socket";

type SocketEvento =
    | "processando"
    | "buscando_arquivos"
    | "gerando_resposta"
    | "chunk_resposta"
    | "resposta_finalizada"
    | "processo_completo"
    | "erro"
    | null;

export default function Chat() {
    const messageFieldRef = useRef<MessageFieldRef>(null);
    const [temMensagem, setTemMensagem] = useState(false);
    const [text, setText] = useState("");
    const [podeEnviarMensagem, setPodeEnviarMensagem] = useState(true);
    const [mensagemPendente, setMensagemPendente] = useState("");
    const [permitido, setPermitido] = useState(true);
    const [eventoAtual, setEventoAtual] = useState<SocketEvento>(null);
    const [chatId, setChatId] = useState<string | null>(null);
    const [materiaIdSelecionada, setMateriaIdSelecionada] = useState<string>("");

    // Flag para saber se já foi criada a bolha da LLM no MessageField
    const llmBolhaCriada = useRef(false);

    const { user } = useAuth();
    const { materias } = useData();

    // Inicializa o materia_id com a primeira matéria disponível
    useEffect(() => {
        if (materias && materias.length > 0 && !materiaIdSelecionada) {
            setMateriaIdSelecionada(materias[0].id);
        }
    }, [materias]);

    // Registro dos listeners do socket
    useEffect(() => {
        socket.connect();

        socket.on("processando", () => {
            setEventoAtual("processando");
        });

        socket.on("buscando_arquivos", () => {
            setEventoAtual("buscando_arquivos");
        });

        socket.on("gerando_resposta", () => {
            setEventoAtual("gerando_resposta");
            messageFieldRef.current?.addMessage("llm", "");
            llmBolhaCriada.current = true;
        });

        socket.on("chunk_resposta", (data: { chunk: string }) => {
            setEventoAtual("chunk_resposta");
            if (!llmBolhaCriada.current) {
                messageFieldRef.current?.addMessage("llm", data.chunk);
                llmBolhaCriada.current = true;
            } else {
                const mensagens = messageFieldRef.current?.getAllMessages() ?? [];
                const ultimoConteudo = mensagens[mensagens.length - 1]?.content ?? "";
                messageFieldRef.current?.updateLastMessage(ultimoConteudo + data.chunk);
            }
        });

        socket.on("resposta_finalizada", (data: { resposta: string }) => {
            setEventoAtual("resposta_finalizada");
            messageFieldRef.current?.updateLastMessage(data.resposta);
            llmBolhaCriada.current = false;
        });

        socket.on("processo_completo", (data: { chatId: string; resposta_completa: string }) => {
            setEventoAtual(null);
            setChatId(data.chatId);
            setPodeEnviarMensagem(true);
        });

        socket.on("erro", (data: { erro: string }) => {
            setEventoAtual("erro");
            llmBolhaCriada.current = false;
            setPodeEnviarMensagem(true);
            console.error("[Socket erro]", data.erro);
        });

        return () => {
            socket.off("processando");
            socket.off("buscando_arquivos");
            socket.off("gerando_resposta");
            socket.off("chunk_resposta");
            socket.off("resposta_finalizada");
            socket.off("processo_completo");
            socket.off("erro");
            socket.disconnect();
        };
    }, []);

    const handleSend = () => {
        if (text.trim() === "" || !podeEnviarMensagem) return;
        if (!materiaIdSelecionada) return;

        const historico = messageFieldRef.current?.getAllMessages() ?? [];

        const payload = {
            id_usuario: user?.id,
            materia_id: materiaIdSelecionada,
            mensagem: text,
            historico: historico ?? [],
            chat_novo: chatId === null,
            id_chat: chatId ?? undefined,
            data_envio: new Date().toISOString(),
        };

        if (!temMensagem) {
            setMensagemPendente(text);
            setTemMensagem(true);
        } else {
            messageFieldRef.current?.addMessage("user", text);
        }

        setText("");
        setPodeEnviarMensagem(false);
        llmBolhaCriada.current = false;

        socket.emit("mensagem_inicial", payload);
    };

    useEffect(() => {
        if (temMensagem && mensagemPendente) {
            messageFieldRef.current?.addMessage("user", mensagemPendente);
            setMensagemPendente("");
        }
    }, [temMensagem, mensagemPendente]);

    useEffect(() => {
        messageFieldRef.current?.deleteAllMessages();
        setTemMensagem(false);
        setText("");
        setPodeEnviarMensagem(true);
        setChatId(null);
        llmBolhaCriada.current = false;
        if (materias == null) {
            setPermitido(false);
        }
    }, []);

    return (
        <>
            <Header
                isSelectInactive={temMensagem && (materias && materias.length > 0)}
                materiaName=""
                onMateriaChange={(id) => setMateriaIdSelecionada(id)}
            />
            {materias && materias.length > 0 && (
                temMensagem
                    ? <MessageField ref={messageFieldRef} />
                    : <NoMessageField
                        onAskQuestion={() => { setText(promptQuestion) }}
                        onSummarize={() => { setText(promptSummarize) }}
                        onPrepareExam={() => { setText(promptExam) }}
                        onDeepDive={() => { setText(promptDeep); }}
                    />
            )}
            {materias && materias.length > 0 && (
                <TextArea
                    value={text}
                    onChange={setText}
                    onSend={handleSend}
                    isDisabled={!podeEnviarMensagem}
                />
            )}
            {materias && materias.length > 0 && (
                <ErrorField temErro={!podeEnviarMensagem} />
            )}
            {materias && materias.length <= 0 && (
                <section className={styles.noMateriaSection}>
                    <section>
                        <p>Você ainda não está matriculado em nenhuma matéria.</p>
                        <p>Entre em contato com a coordenação.</p>
                    </section>
                </section>
            )}
        </>
    )
}
