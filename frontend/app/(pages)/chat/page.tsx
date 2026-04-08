"use client";

import socket from "@/libs/socket";
import { useEffect, useRef, useState } from "react";
import TextAreaChat from "./components/TextAreaChat/TextAreaChat";
import MessageField, { MessageFieldRef } from "./components/MessageField/MessageField";
import SelectMateria from "./components/SelectMateria/SelectMateria";
import HeaderChat from "./components/HeaderChat/HeaderChat";
import styles from "./page.module.css";

export default function Home(){

    const [showSelectMaterias, setShowSelectMaterias] = useState(false);

    //buscar as matérias do aluno/professor aqui
    const materias = {
        "id-mat-1": "Matemática",
        "id-mat-2": "História",
    };

    const handleMateriaChange = (id: string, nome: string) => {
        console.log("Matéria escolhida:", id, nome);
        setShowSelectMaterias(false);
    };
    
    const [text,setText] = useState("");
    
    const messageFieldRef = useRef<MessageFieldRef>(null);

    useEffect(() => {
        if (messageFieldRef.current) {
            messageFieldRef.current.addMessage("user", "Olá! Isso é um teste de interface.");
            messageFieldRef.current.addMessage("llm", "Entendido. A interface está renderizando corretamente!");
            messageFieldRef.current.addMessage("user", "Estou verificando o alinhamento e as cores.");
            messageFieldRef.current.addMessage("llm", "As mensagens de usuário devem ficar de um lado e as minhas de outro.");
            messageFieldRef.current.addMessage("llm", "As mensagens de usuário devem ficar de um lado e as minhas de outro.");
            messageFieldRef.current.addMessage("llm", "As mensagens de usuário devem ficar de um lado e as minhas de outro.");
            messageFieldRef.current.addMessage("llm", "As mensagens de usuário devem ficar de um lado e as minhas de outro.");
            }
    }, []);

    return (
    <>    
        <header className={styles.headerFixo}>
            <HeaderChat
              onNewChatClick={() => console.log("Novo Chat clicado")}
              onUserClick={() => console.log("Usuário clicado")}
              onNavItemClick={(item) => console.log("Item do menu:", item)}
            />
        </header>

        <section className={styles.conteinerMensagens}>
            <MessageField ref={messageFieldRef}/>
        </section>

        {showSelectMaterias && Object.keys(materias).length > 1 &&(
            <SelectMaterias materias={materias} onChange={handleMateriaChange} />
        )}
        
        <footer className={styles.footerFixo}>
            <TextAreaChat
              value={text}
              onChange={setText}
              onSend={() => console.log("Enviar:", text)}
            />
        </footer>
    </>
);
}
