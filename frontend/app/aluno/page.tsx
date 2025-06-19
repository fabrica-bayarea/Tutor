'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';

import Aside from './components/Aside/Aside';

export default function Home() {
    const [aluno, setAluno] = useState({ id: 'cde982bc-2c4b-43a0-8439-eba9d2149306', matricula: '2314290141', nome: 'Victor Henrique', email: 'victor@gmail.com' }); // ...senha, cpf, data_nascimento
    return (
        <div className={styles.pageContainer}>
            <Aside selected='home' />
            <div className={styles.midColumn}>
                <div className={styles.header}>
                    <h1>Olá, {aluno.nome}!</h1>
                </div>
            </div>
        </div>
    )
}
