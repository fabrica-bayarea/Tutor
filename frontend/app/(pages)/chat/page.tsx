"use client";

import socket from "@/libs/socket";
import { useEffect, useRef, useState } from "react";
import TextAreaChat from "./components/TextAreaChat/TextAreaChat";
import MessageField, { MessageFieldRef } from "./components/MessageField/MessageField";
import SelectMateria from "./components/SelectMateria/SelectMateria";
import HeaderChat from "./components/HeaderChat/HeaderChat";
import styles from "./page.module.css";
import { useRouter } from "next/navigation";
import { logoutAluno } from "@/app/services/service_aluno";
import { useAuth } from "@/contexts/AuthContext";

export default function Home() {
    const router = useRouter();
    const messageFieldRef = useRef<MessageFieldRef>(null);
    const [showSelectMaterias, setShowSelectMaterias] = useState(true);
    const [text, setText] = useState("");
    const [isTextAreaDisabled, setTextAreaDisabled] = useState(false);
    const [idMateria, setIdMateria] = useState("");
    const [chatNovo, setChatNovo] = useState(true);
    const [idChat, setIdChat] = useState("");
    const { aluno, setAluno, loading } = useAuth();

    if (loading || !aluno) return null;
    
    const materias = { "id-mat-1": "Matemática", "id-mat-2": "História", };//buscar as matérias do aluno/professor aqui

    const handleMateriaChange = (id: string, nome: string) => {
        setShowSelectMaterias(false);
        setIdMateria(id);
    };

    const handleNovoChat = () => {
        messageFieldRef.current?.deleteAllMessages();
        setIdMateria("")
        setIdChat("")
        setChatNovo(true);
    };

    const handleConfig = () => {
        console.log("Abrir configurações");
    };

    const handleSair = async () => {
        try {
          await logoutAluno();
          setAluno(null);
          router.replace("/login");
        } catch (error) {
          console.error("Erro ao sair:", error);
        }
      };

    const handleDash = () => {
        console.log("Abrir Dashboard");
    };

    const handleSend = (text: string) => {
        if(!text.trim()) return;

        messageFieldRef.current?.addMessage("user",text);
        messageFieldRef.current?.addMessage("llm","...");

        console.log("Adicionar aqui a lógica de socket de envio de mensagem.");

        //após a lógica de envio
        if(chatNovo){
            setIdChat("id-do-chat-recebido-novo")
            setChatNovo(false);
        }
        setText("");
    }

    useEffect(() => {
        socket.on("processando", () => {
            messageFieldRef.current?.updateLastMessage("Mensagem em processamento...");
            setTextAreaDisabled(true)
        });

        socket.on("buscando_material", () => {
            messageFieldRef.current?.updateLastMessage("Buscando material semântico...");
        });

        socket.on("gerando_resposta", () => {
            messageFieldRef.current?.updateLastMessage("Gerando resposta...");
        });

        socket.on("processo_completo", () => {
            setTextAreaDisabled(false)
        });

        socket.on("erro", () => {
            messageFieldRef.current?.updateLastMessage("Não foi possível gerar sua resposta, tente novamente.");
            setTextAreaDisabled(false)
        });
        return () => {
            socket.off("processando");
            socket.off("buscando_material");
            socket.off("gerando_resposta");
            socket.off("processo_completo");
            socket.off("erro");
        };

    }, [])

    return (
        <>
            <header className={styles.headerFixo}>
                <HeaderChat
                    onNewChatClick={handleNovoChat}
                    onNavItemClick={(item) => {
                        if (item === "Sair") handleSair();
                        if (item == "Configurações") handleConfig();
                        if (item == "Dashboard") handleDash();
                    }}
                />
            </header>

            <section className={styles.conteinerMensagens}>
                <MessageField ref={messageFieldRef} />
            </section>

            {showSelectMaterias && Object.keys(materias).length > 1 && (
                <SelectMateria materias={materias} onChange={handleMateriaChange} />
            )}

            <footer className={styles.footerFixo}>
                <TextAreaChat
                    isDisabled={isTextAreaDisabled}
                    value={text}
                    onChange={setText}
                    onSend={(text) => handleSend(text)}
                />
            </footer>
        </>
    );
}
