'use client';

import { useEffect, useState } from "react"
import Aside from "./components/Aside/Aside"
import styles from "./layout.module.css"
import { InterfaceAluno, InterfaceChat } from "../../types"
import { obterChats } from "../../services/service_chat"
import socket from "@/libs/socket"

export default function AlunoLayout({ children }: { children: React.ReactNode }) {
    const [aluno, setAluno] = useState<InterfaceAluno | null>(null)
    const [chats, setChats] = useState<InterfaceChat[]>([])

    useEffect(() => {
        const alunoData = localStorage.getItem("aluno")
        if (alunoData) {
            try {
                const parsed = JSON.parse(alunoData)
                setAluno(parsed)
                obterChats(parsed.id).then(setChats).catch(console.error)
            } catch (err) {
                console.error("Erro ao parsear aluno:", err)
            }
        }
    }, [])

    // Listeners para eventos emitidos pelo back-end
    useEffect(() => {
        socket.on("novo_chat", (chat: InterfaceChat) => {
            setChats(prev => [...prev, chat])
        })
    }, [])

    return (
        <main className={styles.pageContainer}>
            <Aside chats={chats} />
            <div className={styles.midColumnContainer}>{children}</div>
        </main>
    )
}
