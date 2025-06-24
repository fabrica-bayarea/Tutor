'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';
import MessageForm from './components/MessageForm/MessageForm';

import { InterfaceAluno } from '../types';

export default function Home() {
    const [aluno, setAluno] = useState<InterfaceAluno>({ id: 'cde982bc-2c4b-43a0-8439-eba9d2149306', matricula: '2314290141', nome: 'Victor', email: 'victor@gmail.com', cpf: '12345678901', data_nascimento: new Date('2000-01-01') }); // ...senha, cpf, data_nascimento
    
    useEffect(() => {
        
    }, []);
    
    function sendMessage(message: string) {
        console.log(message);
    }
    
    return (
        <div className={styles.midColumn}>
            <div className={styles.headerContainer}>
                <h1>Olá, {aluno.nome}!</h1>
                <h2>Como posso ajudar hoje?</h2>
            </div>
            <div className={styles.bottomContainer}>
                <MessageForm onSendMessage={sendMessage} />
                <span>A inteligência artificial pode cometer erros. Considere checar informações importantes.</span>
            </div>
        </div>
    )
}
