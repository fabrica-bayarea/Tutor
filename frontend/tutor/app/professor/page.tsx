'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';

import Aside from './components/Aside/Aside';

export default function Home() {
    const [professor, setProfessor] = useState({ id: '550e8400-e29b-41d4-a716-446655440000', matricula: '1', nome: 'Regiano', email: 'regiano@gmail.com' }); // ...senha, cpf, data_nascimento
    return (
        <div className={styles.pageContainer}>
            <Aside selected='home' />
            <div className={styles.midColumn}>
                <div className={styles.header}>
                    <h1>Olá, {professor.nome}!</h1>
                </div>
            </div>
        </div>
    )
}
