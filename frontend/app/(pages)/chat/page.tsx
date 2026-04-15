"use client";

    import socket from "@/libs/socket";
    import { useEffect, useRef, useState } from "react";
    import TextAreaChat from "./components/TextAreaChat/TextAreaChat";
    import MessageField, { MessageFieldRef } from "./components/MessageField/MessageField";
    import SelectMateria from "./components/SelectMateria/SelectMateria";
    import HeaderChat from "./components/HeaderChat/HeaderChat";
    import styles from "./page.module.css";
    import { useAuth } from "@/utils/auth";

    export default function Home() {
        const messageFieldRef = useRef<MessageFieldRef>(null);
        const [showSelectMaterias, setShowSelectMaterias] = useState(true);
        const [text, setText] = useState("");
        const [isTextAreaDisabled, setTextAreaDisabled] = useState(false);
        const [newChat, setNewChat] = useState(true);
        const [materia, setMateria] = useState("");
        const [nomeMateria, setNomeMateria] = useState("");
        const [chat,setChat] = useState("");
        const { user, loading, isAuthenticated, isStudent, isProfessor, isAdmin } = useAuth();
        const [respostaAtual, setRespostaAtual] = useState("");

        const materias = {"id-mat-1": "Matemática","id-mat-2": "Física"};//buscar as matérias do aluno/professor aqui

        const handleMateriaChange = (id: string, nome: string) => {
            setMateria(id);
            setNomeMateria(nome);
            setShowSelectMaterias(false);
        };

        useEffect(() => {
            if(newChat) setShowSelectMaterias(true);
        },[newChat])

        const handleNovoChat = () => {
            messageFieldRef.current?.deleteAllMessages();
            setNewChat(true);
            setShowSelectMaterias(true);
            setTextAreaDisabled(false);
        };

        const handleConfig = () => {
            console.log("Abrir configurações");
        };

        const handleSair = () => {
            console.log("Encerrar sessão");
        };

        const handleDash = () => {
            console.log("Abrir Dashboard");
        };

        const handleSend = (text: string) => {
            if(text.trim() == "") return;
            setTextAreaDisabled(true)
            messageFieldRef.current?.addMessage("user",text);
            setText("");
            messageFieldRef.current?.addMessage("llm","");

            socket.emit("mensagem_inicial", {
                id_usuario: user?.id,
                id_materia: materia,
                mensagem: text,
                historico: messageFieldRef.current?.getAllMessages(),
                chat_novo: newChat,
                id_chat: newChat ? null : chat,
                data_envio: "2026-03-22T19:20:24Z"
            });

            setNewChat(false);
            setChat("idDoChat")
        }

        useEffect(() => {
            socket.on("processando", () => {
                messageFieldRef.current?.updateLastMessage("Mensagem em processamento...");
                setTextAreaDisabled(true)
            });

            socket.on("chunk_mensagem", (data: { data: any; }) => {
                const chunk = data.data;
            
                setRespostaAtual((prev) => {
                    const nova = prev + chunk;
            
                    messageFieldRef.current?.updateLastMessage(nova);
            
                    return nova;
                });
            });

            socket.on("processo_completo", () => {
                setTextAreaDisabled(false);
                setRespostaAtual("");
            });

            socket.on("erro", () => {
                messageFieldRef.current?.updateLastMessage("Não foi possível gerar sua resposta, tente novamente.");
                setTextAreaDisabled(false);
                setRespostaAtual("");
            });
            return () => {
            
                socket.off("processando")
                socket.off("processo_completo")
                socket.off("erro")
                socket.off("chunk_mensagem")
                socket.off("processo_completo")
            }
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

                {showSelectMaterias && (
                    <SelectMateria materias={materias} onChange={handleMateriaChange} />
                )}

                <div className={styles.materiaBackground}>
                    {nomeMateria}
                </div>


                <footer className={styles.footerFixo}>
                    <TextAreaChat
                        isDisabled={isTextAreaDisabled}
                        value={text}
                        onChange={setText}
                        onSend={() => handleSend(text)}
                    />
                </footer>
            </>
        );
    }