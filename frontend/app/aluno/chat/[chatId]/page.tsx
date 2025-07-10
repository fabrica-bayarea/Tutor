"use client";

import { useEffect, useState, useRef } from "react"
import { useParams } from "next/navigation"

import MessageBox from "../../components/MessageBox/MessageBox"
import MessageForm from "../../components/MessageForm/MessageForm"
import styles from "./page.module.css"
import socket from "@/libs/socket"

import { InterfaceAluno, InterfaceMensagem } from "../../../types"
import { LLM_UUID } from "@/constants"
import { obterMensagens } from "@/app/services/service_mensagem"

export default function ChatPage() {
    const { chatId } = useParams()

    const [aluno, setAluno] = useState<InterfaceAluno | null>(null)
    const [mensagens, setMensagens] = useState<InterfaceMensagem[]>([])
    const [gerandoResposta, setGerandoResposta] = useState(false)
    const [mensagemGerada, setMensagemGerada] = useState<InterfaceMensagem | null>(null)

    const mensagemGeradaRef = useRef<InterfaceMensagem | null>(null)
    const chunkBuffer = useRef<string[]>([]) // Buffer para chunks que chegarem antes da estrutura inicial da mensagem da LLM

    useEffect(() => {
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

    // Listeners para eventos emitidos pelo back-end
    useEffect(() => {
        socket.on("mensagem_aluno", (mensagem: InterfaceMensagem) => {
            console.log(`Nova mensagem recebida:\n${mensagem}`)
            setMensagens(prev => [...prev, mensagem])
        })

        socket.on("res_mensagem", (mensagem: InterfaceMensagem) => {
            console.log(`Nova mensagem recebida:\n${mensagem}`)

            setMensagens(prev =>
                prev.map(m => (m.id === "" ? mensagem : m))
            )
        })

        socket.on("resposta_inicio", (resposta: InterfaceMensagem) => {
            console.log(`Nova resposta à caminho:\n${JSON.stringify(resposta)}`)
            setMensagemGerada(resposta)
        })

        socket.on("resposta_chunk", (chunk: string) => {
            console.log(`Novo chunk recebido:\n${chunk}`)
            if (mensagemGeradaRef.current) {
                setMensagemGerada(prev => ({
                    ...prev!,
                    conteudo: prev!.conteudo + chunk
                }))
            } else {
                // Ainda não recebemos a estrutura inicial da mensagem da LLM, então vamos guardar o chunk
                chunkBuffer.current.push(chunk)
            }
        })

        socket.on("resposta_fim", (resposta: InterfaceMensagem) => {
            console.log(`Resposta final recebida:\n${JSON.stringify(resposta)}`)
            setMensagens(prev => [...prev, resposta])
            setMensagemGerada(null)
            setGerandoResposta(false)
        })

        socket.on("erro", (error: string) => {
            console.error(`Erro recebido:\n${error}`)
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
    }, [])

    useEffect(() => {
        const carregarMensagens = async () => {
            try {
                const mensagensRecebidas = await obterMensagens(chatId as string)
                setMensagens(mensagensRecebidas)
            } catch (error) {
                console.error("Erro ao carregar mensagens:", error)
            }
        }

        carregarMensagens()
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

    return (
        <div className={styles.midColumn}>
            <div className={styles.topContainer}>
                <div className={styles.messagesContainer}>
                    {mensagens.map(msg => (
                        <MessageBox key={msg.id} {...msg} />
                    ))}
                    {gerandoResposta && mensagemGeradaRef.current && (
                        <MessageBox {...mensagemGeradaRef.current} />
                    )}
                </div>
            </div>
            <div className={styles.bottomContainer}>
                <MessageForm onSendMessage={handleEnviar} />
                <span>A inteligência artificial pode cometer erros. Considere checar informações importantes.</span>
            </div>
        </div>
    )
}
