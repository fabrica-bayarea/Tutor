"use client";

import socket from "@/libs/socket";
import { useEffect, useRef, useState } from "react";
import TextAreaChat from "./components/TextAreaChat/TextAreaChat";
import MessageField, { MessageFieldRef } from "./components/MessageField/MessageField";
import SelectMateria from "./components/SelectMateria/SelectMateria";
import HeaderChat from "./components/HeaderChat/HeaderChat";
import styles from "./page.module.css";

export default function Home(){
    const messageFieldRef = useRef<MessageFieldRef>(null);
    const [showSelectMaterias, setShowSelectMaterias] = useState(false);
    const [text,setText] = useState("");

    const materias = {"id-mat-1": "Matemática","id-mat-2": "História",};//buscar as matérias do aluno/professor aqui

    const handleMateriaChange = (id: string, nome: string) => {
        setShowSelectMaterias(false);
    };

    const handleNovoChat = () => {
        console.log("Realizar sequência de novo chat");
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
            <MessageField ref={messageFieldRef}/>
        </section>

        {showSelectMaterias && Object.keys(materias).length > 1 &&(
            <SelectMateria materias={materias} onChange={handleMateriaChange} />
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
