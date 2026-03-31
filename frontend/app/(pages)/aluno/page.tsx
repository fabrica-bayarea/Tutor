"use client";

import { useEffect, useState } from "react"
import MessageForm from "./components/MessageForm/MessageForm"
import styles from "./page.module.css"
import socket from "@/libs/socket"
import { useRouter } from "next/navigation"
import { InterfaceUsuario, InterfaceChat } from "../../types"
import Select from 'react-select';
import UserButton from "@/app/components/UserButton/userButton";
import Spinner from "@/app/components/Spinner/Spinner";

export default function Home() {
    const router = useRouter()
    const [isMounted, setIsMounted] = useState(false);
    const [aluno, setAluno] = useState<InterfaceUsuario | null>(null)
    const [isProcessing, setIsProcessing] = useState(false);

    useEffect(() => {
        setIsMounted(true);
        const alunoData = localStorage.getItem("aluno")
        if (alunoData) {
            try {
                setAluno(JSON.parse(alunoData))
            } catch (err) {
                console.error("Erro ao parsear aluno:", err)
            }
        }
    }, []);

    useEffect(() => {
        const handleProcessando = () => {
            setIsProcessing(true);
        };

        window.addEventListener("processando", handleProcessando);
        return () => window.removeEventListener("processando", handleProcessando);
    }, []);

    // Listeners para eventos emitidos pelo back-end
    useEffect(() => {
        socket.on("novo_chat", (chat: InterfaceChat) => {
            console.log(`Novo chat recebido:\n${JSON.stringify(chat)}`)
            console.log(`Redirecionando para '/aluno/chat/${chat.id}'`)
            router.push(`/aluno/chat/${chat.id}?novo=true`)
        })
    }, []);

    const handleEnviarMensagemInicial = (msg: string) => {
        if (aluno) {
            console.log(`Enviando mensagem inicial: ${msg}`)
            socket.emit("mensagem_inicial", {
                aluno_id: aluno.id,
                mensagem: msg,
            })
        }
    }
    if (!isMounted) return null;
    return (
        <>
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
                {isProcessing ? (
                    <Spinner message="Preparando chat no servidor..." />
                ) : (
                    <MessageForm onSendMessage={handleEnviarMensagemInicial} isDisabled={isProcessing}/>
                )}
                <span>A inteligência artificial pode cometer erros. Considere checar informações importantes.</span>
            </div>
        </div>
        <UserButton user={aluno?.nome.split(' ')[0]}  isProf={aluno?.role == 'RoleEnum.ADMIN' || aluno?.role == 'RoleEnum.PROFESSOR'}/>
        </>
    )
}
