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
        const { materias, turmas } = useData();

        const materiasMap = useMemo(() => {
            if(materias.length === 0) return { "132123123124123": "Estatística" };
            return Object.fromEntries(
                materias.map(m => [m.id.toString(), m.nome])
              );
        }, [materias]);

        useEffect(()=>{console.log(materiaId),[materiaId]};
                  
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
            messageFieldRef.current?.addMessage("llm","...");

            socket.emit("nova_mensagem", {
                id_usuario: user?.id,
                id_materia: materiaId,
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
            
                socket.off("processando")
                socket.off("buscando_material")
                socket.off("gerando_resposta")
                socket.off("processo_completo")
                socket.off("erro")
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
