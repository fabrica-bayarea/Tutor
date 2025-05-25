"use client" // Componente de renderização 

import styles from "./paginaInicial.module.css";  // Import os estilos CSS
import sendImage from "../assets/send.png"     // Imagem de send
import React from 'react'; // Importa React e hooks

export default function PaginaInicial() {
    // Desestrutura funções e variáveis do contexto ModalContext
    return (
        <div className={styles.containerGlobal}> {/* Container principal da página */}
            <h1 className={styles.titulo}>Olá, -Nome-<br/><p>Como eu posso te ajudar hoje?</p></h1>
            {/* Área principal do chat do usuário */}
            <div className={styles.containerUser}>
                <div className={styles.containerChatMessage}></div> {/* Mensagens do chat (ainda vazio) */}
                <div className={styles.containerChatBox}>
                    {/* Área de texto para digitação de mensagens */}
                    <textarea
                        placeholder="Digite uma mensagem"
                        minLength={10}
                    />
                    <button className={styles.buttonSend}>
                        <img src={sendImage.src} width={30} height={30} />
                    </button>
                </div>
            </div>
        </div>
    );
};