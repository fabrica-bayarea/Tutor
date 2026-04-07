"use client";

import socket from "@/libs/socket";
import { useEffect, useState } from "react";
import TextAreaChat from "./Components/TextAreaChat/TextAreaChat";
import MessageField from "./Components/MessageField/MessageField";
import HeaderChat from "./components/HeaderChat/HeaderChat";
import styles from "./page.modules.css";

export default function Home(){

    const messageFieldRef = useRef<MessageFieldRef>(null);

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
