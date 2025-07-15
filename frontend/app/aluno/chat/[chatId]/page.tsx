"use client";

import { useEffect, useState, useRef } from "react"
import { useParams, useSearchParams } from "next/navigation"

import MessageBox from "../../components/MessageBox/MessageBox"
import MessageForm from "../../components/MessageForm/MessageForm"
import styles from "./page.module.css"
import socket from "@/libs/socket"

import { InterfaceAluno, InterfaceMensagem } from "../../../types"
import { LLM_UUID } from "@/constants"
import { obterMensagens } from "@/app/services/service_mensagem"

export default function ChatPage() {
    const { chatId } = useParams()
    const searchParams = useSearchParams()
    const novoChat = searchParams.get("novo") === "true";
    const prontoEmitido = useRef<boolean>(false)

    const [aluno, setAluno] = useState<InterfaceAluno | null>(null)
    const [mensagens, setMensagens] = useState<InterfaceMensagem[]>([])
    const [gerandoResposta, setGerandoResposta] = useState<boolean>(false)
    const [mensagemGerada, setMensagemGerada] = useState<InterfaceMensagem | null>(null)

    const idMensagemGeradaRef = useRef<string | null>(null)
    const mensagemGeradaRef = useRef<InterfaceMensagem | null>(null)
    const chunkBuffer = useRef<string[]>([]) // Buffer para chunks que chegarem antes da estrutura inicial da mensagem da LLM

    useEffect(() => {
        console.log("mensagemGerada atualizada:", mensagemGerada?.conteudo)
        mensagemGeradaRef.current = mensagemGerada;

        // Se recebemos chunks antes de receber a estrutura da mensagem da LLM, agora podemos usá-los
        if (mensagemGerada && chunkBuffer.current.length > 0) {
            const chunks = [...chunkBuffer.current];
            chunkBuffer.current = [];

            chunks.forEach(chunk => {
                setMensagemGerada(prev => ({
                    ...prev!,
                    conteudo: prev!.conteudo + chunk
                }))
            })
        }
    }, [mensagemGerada]);

    useEffect(() => {
        const alunoData = localStorage.getItem("aluno")
        if (alunoData) setAluno(JSON.parse(alunoData))
    }, [])

    useEffect(() => {
        // Se for um chat novo, emite um "handshake" para o back-end para receber a mensagem inicial e a resposta da LLM
        if (novoChat && !prontoEmitido.current) {
            socket.emit("pronto_para_receber")
            console.log("Emitido: pronto_para_receber")
            prontoEmitido.current = true
        } else if (!novoChat && chatId) { // Se não, busca todas as mensagens do chat no banco de dados
            const carregarMensagens = async () => {
                try {
                    const mensagensRecebidas = await obterMensagens(chatId as string)
                    setMensagens(mensagensRecebidas)
                } catch (error) {
                    console.error("Erro ao carregar mensagens:", error)
                }
            }

            carregarMensagens()
        }
    }, [chatId, novoChat])

    // Listeners para eventos emitidos pelo back-end
    useEffect(() => {
        // Listener para pegar a mensagem inicial do aluno, enviada em outra página, após ser devidamente salva no banco de dados
        socket.on("mensagem_aluno", (mensagem: InterfaceMensagem) => {
            console.log(`Nova mensagem inicial recebida:\n${JSON.stringify(mensagem)}`)
            setMensagens(prev => [...prev, mensagem])
        })

        // Listener para receber mensagens subsequentes enviadas próprio aluno, após serem devidamente salvas no banco de dados
        socket.on("res_mensagem", (mensagem: InterfaceMensagem) => {
            console.log(`Nova mensagem subsequente recebida:\n${JSON.stringify(mensagem)}`)

            setMensagens(prev =>
                prev.map(m => (m.id === "" ? mensagem : m))
            )
        })

        // Listener para receber o ID da mensagem da LLM, sinalizando que a resposta começou a ser gerada
        // A ideia desse listener é criar uma mensagem parcial usando esse ID, e atualizá-la em tempo real com os chunks recebidos em eventos 'resposta_chunk'
        socket.on("resposta_inicio", (id_mensagem_llm: string) => {
            console.log(`ID da nova resposta da LLM recebido:\n${id_mensagem_llm}`)
            idMensagemGeradaRef.current = id_mensagem_llm;
            const respostaParcial: InterfaceMensagem = {
                id: id_mensagem_llm,
                chat_id: chatId as string,
                sender_id: LLM_UUID,
                conteudo: "",
                data_envio: new Date()
            }
            mensagemGeradaRef.current = respostaParcial;
            setMensagens(prev => [...prev, respostaParcial])
        })

        // Listener para receber chunks da resposta da LLM, atualizando a mensagem parcial em tempo real
        socket.on("resposta_chunk", (chunk: string) => {
            console.log(`Novo chunk recebido:\n${chunk}`)
            const id = idMensagemGeradaRef.current;

            if (id) {
                setMensagens((prev) =>
                    prev.map((m) =>
                        m.id === id ? { ...m, conteudo: m.conteudo + chunk } : m
                    )
                )
            } else {
                console.log(`Chunk ${chunk} chegou muito cedo. Adicionando ao Buffer`)
                chunkBuffer.current.push(chunk)
                console.log(`Buffer atual: ${chunkBuffer.current}`)
            }
        })

        // Listener para receber a resposta final da LLM com estrutura completa e substituir a mensagem parcial que estava sendo gerada
        socket.on("resposta_fim", (resposta: InterfaceMensagem) => {
            console.log(`Resposta final recebida:\n${JSON.stringify(resposta)}`)
            const id = idMensagemGeradaRef.current;
            setMensagens((prev) =>
                prev.map((m) => (m.id === id ? resposta : m))
            );
            setGerandoResposta(false);
            idMensagemGeradaRef.current = null;
            console.log(`Resposta final recebida:\n${JSON.stringify(resposta)}`)
        })

        socket.on("erro", (error: any) => {
            console.error(`Erro recebido:\n${JSON.stringify(error)}`)
            setGerandoResposta(false)
        })

        return () => {
            // Limpeza para evitar múltiplos listeners em hot reload
            socket.off("mensagem_aluno")
            socket.off("res_mensagem")
            socket.off("resposta_inicio")
            socket.off("resposta_chunk")
            socket.off("resposta_fim")
            socket.off("erro")
        }
    }, [chatId])

    const handleEnviar = (mensagem: string) => {
        if (aluno) {
            setMensagens(prev => [...prev, {
                id: '',
                chat_id: chatId as string,
                sender_id: aluno.id,
                conteudo: mensagem,
                data_envio: new Date(),
            }])

            socket.emit("nova_mensagem_aluno", {
                chat_id: chatId as string,
                aluno_id: aluno.id,
                mensagem,
            })
            setGerandoResposta(true)
        }
    }

    const bottomRef = useRef<HTMLDivElement>(null)
    
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [mensagens])

    return (
        <div className={styles.midColumn}>
            <div className={styles.topContainer}>
                <div className={styles.messagesContainer}>
                    {mensagens.map(msg => (
                        <MessageBox
                            key={msg.id}
                            id={msg.id}
                            chat_id={msg.chat_id}
                            sender_id={msg.sender_id}
                            conteudo={msg.conteudo}
                            data_envio={msg.data_envio}
                        />
                    ))}
                    <div ref={bottomRef} />
                </div>
            </div>
            <div className={styles.bottomContainer}>
                <MessageForm onSendMessage={handleEnviar} />
                <span>A inteligência artificial pode cometer erros. Considere checar informações importantes.</span>
            </div>
        </div>
    )
}
