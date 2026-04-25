"use client";

    import socket from "@/libs/socket";
    import { useEffect, useRef, useState, useMemo } from "react";
    import TextAreaChat from "./components/TextAreaChat/TextAreaChat";
    import MessageField, { MessageFieldRef } from "./components/MessageField/MessageField";
    import SelectMateria from "./components/SelectMateria/SelectMateria";
    import HeaderChat from "./components/HeaderChat/HeaderChat";
    import styles from "./page.module.css";
    import { useAuth } from "@/utils/auth";
    import { useData } from "@/utils/data";


    export default function Home() {
        const messageFieldRef = useRef<MessageFieldRef>(null);
        const [showSelectMaterias, setShowSelectMaterias] = useState(true);
        const [text, setText] = useState("");
        const [isTextAreaDisabled, setTextAreaDisabled] = useState(false);
        const [newChat, setNewChat] = useState(true);
        const [materiaId, setMateriaId] = useState("");
        const [materiaNome, setMateriaNome] = useState("");
        const [chat,setChat] = useState("");
        const { user, loading, isAuthenticated, isStudent, isProfessor, isAdmin } = useAuth();
        const [respostaAtual, setRespostaAtual] = useState("");
        const { materias, turmas } = useData();

        const materiasMap = useMemo(() => {
            return Object.fromEntries(
                materias.map((m: any) => [m.id.toString(), m.nome])
              );
        }, [materias]);
                  
        const handleMateriaChange = (id: string, nome: string) => {
            setMateriaId(id);
            setMateriaNome(nome);
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
            setChat("");
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
                materia_id: materiaId,
                mensagem: text,
                historico: messageFieldRef.current?.getAllMessages(),
                chat_novo: newChat,
                id_chat: newChat ? null : chat,
                data_envio: "2026-03-22T19:20:24Z"
            });

            setNewChat(false);
            }
        useEffect(() => {
            if (!socket.connected) {
                socket.connect();
            }

            socket.on("connection-confirmation", (data: any) => {
                console.log("Servidor confirmou conexão:", data);
            });

            socket.on("processando", () => {
                messageFieldRef.current?.updateLastMessage("Mensagem em processamento...");
                setTextAreaDisabled(true);
            });

            socket.on("buscando_arquivos", () => {
                messageFieldRef.current?.updateLastMessage("Realizando busca semântica...");
            });

            socket.on("gerando_resposta", () => {
                messageFieldRef.current?.updateLastMessage("Gerando resposta...");
            });

            socket.on("chunk_mensagem", (data: { data: any }) => {
                const chunk = data.data;

                setRespostaAtual((prev: any) => {
                    const nova = prev + chunk;
                    messageFieldRef.current?.updateLastMessage(nova);
                    return nova;
                });
            });

            socket.on("processo_completo", (data: {chatId: string}) => {
                setTextAreaDisabled(false);
                setRespostaAtual("");
                setChat(data.chatId)
            });

            socket.on("erro", (data: { erro?: string }) => {
                const mensagem = data?.erro || "Erro desconhecido";

                messageFieldRef.current?.updateLastMessage("Erro: " + mensagem);
                setTextAreaDisabled(false);
                setRespostaAtual("");
            });
            return () => {
                socket.off("connection-confirmation");
                socket.off("processando");
                socket.off("buscando_arquivos");
                socket.off("buscando_vetores");
                socket.off("formatando_chunks");
                socket.off("construindo_prompt");
                socket.off("processo_completo");
                socket.off("erro");
                socket.off("chunk_mensagem");
            }
        }, [])

        return (
            <>
                <header className={styles.headerFixo}>
                    <HeaderChat
                        isDisabled={isTextAreaDisabled}
                        onNewChatClick={handleNovoChat}
                        onNavItemClick={(item) => {
                            if (item === "Sair") handleSair();
                            if (item == "Configurações") handleConfig();
                            if (item == "Dashboard") handleDash();
                        }}
                        isAdmin={isAdmin || isProfessor}
                    />
                </header>

                <section className={styles.conteinerMensagens}>
                    <MessageField ref={messageFieldRef} />
                </section>

                {showSelectMaterias && (
                    <SelectMateria 
                        materias={materiasMap} 
                        onChange={handleMateriaChange} />
                )}

                <div className={styles.materiaBackground}>
                    {materiaNome}
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
