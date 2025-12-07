"use client";

import { useEffect, useState } from "react"
import MessageForm from "./MessageForm/MessageForm"
import styles from "./page.module.css"
import socket from "@/libs/socket"
import { useRouter } from "next/navigation"
import { InterfaceAluno, InterfaceChat } from "../../../types"
import AsideChat from "../components/AsideChat/AsideChat";
import Select from 'react-select';
import UserButton from "../../../components/UserButton/userButton";

export default function Home() {
    const router = useRouter()
    const [aluno, setAluno] = useState<InterfaceAluno | null>(null)

    useEffect(() => {
        const alunoData = localStorage.getItem("aluno")
        if (alunoData) {
            try {
                setAluno(JSON.parse(alunoData))
            } catch (err) {
                console.error("Erro ao parsear aluno:", err)
            }
        }
    }, [])

    // Listeners para eventos emitidos pelo back-end
    useEffect(() => {
        socket.on("novo_chat", (chat: InterfaceChat) => {
            console.log(`Novo chat recebido:\n${JSON.stringify(chat)}`)
            console.log(`Redirecionando para '/aluno/chat/${chat.id}'`)
            router.push(`/aluno/chat/${chat.id}?novo=true`)
        })
    }, [])

    const handleEnviarMensagemInicial = (msg: string) => {
        if (aluno) {
            console.log(`Enviando mensagem inicial: ${msg}`)
            socket.emit("mensagem_inicial", {
                aluno_id: aluno.id,
                mensagem: msg,
            })
        }
    }

    return (
        <>
        <AsideChat chats={[]}/>
        <div className={styles.midColumn}>
                <div className={styles.materiaFilter}>
                    <Select
                        isMulti
                        placeholder="Todas as matérias"
                        //options={options}
                        //onChange={handleVinculosChange}
                    />
                </div>
            <div className={styles.headerContainer}>
                <h1>Olá, {aluno?.nome}!</h1>
                <h2>Como posso ajudar hoje?</h2>
            </div>
            <div className={styles.bottomContainer}>
                <MessageForm onSendMessage={handleEnviarMensagemInicial} />
                <span>A inteligência artificial pode cometer erros. Considere checar informações importantes.</span>
            </div>
        </div>
        <UserButton isProf={true} user="professor"/>
        </>
    )
}