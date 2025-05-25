"use client" // Componente de renderização

import styles from "./paginaInicial.module.css";
import sendImage from "../assets/send.png"
import React, { useState, KeyboardEventHandler, MouseEventHandler, useRef, useEffect } from 'react';

interface Message {
  text: string;
  sender: 'user' | 'system';
}

export default function PaginaInicial() {
  const [mensagens, setMensagens] = useState<Message[]>([]);
  const [temtexto, settemtexto] = useState(false);
  const [text, setText] = useState('');
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const addText = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(event.target.value);
  };

  const enviarMensagem = () => {
    settemtexto(true);
    if (text.trim() !== '') {
      setMensagens(prevMensagens => [...prevMensagens, { text: text, sender: 'user' }, { text: 'ok, mensagem recebida', sender: 'system' }]);
      setText('');
    }
  };

  const handleKeyDown: KeyboardEventHandler<HTMLTextAreaElement> = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      settemtexto(true);
      event.preventDefault();
      enviarMensagem();
    }
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [mensagens]);

  return (
    <div className={styles.containerGlobal}>
      {!temtexto &&
        <h1 className={styles.titulo}>Olá, -Nome-<br /><p>Como eu posso te ajudar hoje?</p></h1>
      }
      <div className={styles.containerUser}>
        <div className={styles.containerChatMessage} ref={chatContainerRef}>
          {mensagens.map((msg, index) => (
            <div key={index} className={`${styles.mensagemUsuario} ${msg.sender === 'user' ? styles.mensagemUsuarioEnviada : styles.mensagemSistema}`}>
              <h1>{msg.sender === 'user' ? '-Nome-' : 'Tutor'}</h1>
              <p>{msg.text}</p>
            </div>
          ))}
        </div>
        <div className={styles.containerChatBox}>
          <textarea
            placeholder="Digite uma mensagem"
            minLength={1}
            onKeyDown={handleKeyDown}
            onChange={addText}
            value={text}
          />
          <button className={styles.buttonSend} onClick={enviarMensagem}>
            <img src={sendImage.src} width={30} height={30} alt="Enviar" />
          </button>
        </div>
      </div>
    </div>
  );
};