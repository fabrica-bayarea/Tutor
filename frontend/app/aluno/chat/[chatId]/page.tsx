'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';

import MessageBox from '../../components/MessageBox/MessageBox';
import MessageForm from '../../components/MessageForm/MessageForm';

import { InterfaceAluno, InterfaceMensagem } from '../../../types';

export default function Chat() {
    const [aluno, setAluno] = useState<InterfaceAluno>({ id: 'cde982bc-2c4b-43a0-8439-eba9d2149306', matricula: '2314290141', nome: 'Victor', email: 'victor@gmail.com', cpf: '12345678901', data_nascimento: new Date('2000-01-01') }); // ...senha, cpf, data_nascimento
    const [messages, setMessages] = useState<InterfaceMensagem[]>([
        {
            id: 'b1dd2b7a-a0de-42f3-9ca4-a71a5ff2d94b',
            chat_id: 'af734cdf-1106-49ec-8b26-be87598c992c',
            sender_id: 'cde982bc-2c4b-43a0-8439-eba9d2149306',
            conteudo: 'Olá, mundo!',
            data_envio: new Date('2025-06-03 19:51:25.222023'),
        },
        {
            id: '6fe26828-86b2-4792-ae89-f005a8fdd37b0',
            chat_id: 'af734cdf-1106-49ec-8b26-be87598c992c',
            sender_id: 'ae5905d6-cb44-4884-9408-6fcd7cb3b27c', // UUID único para mensagens da LLM
            conteudo: 'Olá! Como vai?',
            data_envio: new Date('2025-06-03 19:51:26.602426'),
        }
    ]);
    
    useEffect(() => {
        
    }, []);
    
    function sendMessage(message: string) {
        console.log(message);
    }
    
    return (
        <div className={styles.midColumn}>
            <div className={styles.topContainer}>
                <div className={styles.messagesContainer}>
                    {messages.map((message) => (
                        <MessageBox
                            key={message.id}
                            id={message.id}
                            chat_id={message.chat_id}
                            sender_id={message.sender_id}
                            conteudo={message.conteudo}
                            data_envio={message.data_envio}
                        />
                    ))}
                </div>
            </div>
            <div className={styles.bottomContainer}>
                <MessageForm onSendMessage={sendMessage} />
                <span>A inteligência artificial pode cometer erros. Considere checar informações importantes.</span>
            </div>
        </div>
    )
}
