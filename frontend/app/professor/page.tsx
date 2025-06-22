'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';

import { InterfaceProfessor } from '../types';

export default function Home() {
    const [professor, setProfessor] = useState<InterfaceProfessor>({
        id: '550e8400-e29b-41d4-a716-446655440000',
        matricula: '1',
        nome: 'Regiano',
        email: 'regiano@gmail.com',
        cpf: '12345678900', // ...senha, data_nascimento
    });
    
    useEffect(() => {
        
    }, []);
    
    return (
        <div className={styles.midColumn}>
            <div className={styles.header}>
                <h1>Olá, {professor.nome}!</h1>
            </div>
        </div>
    )
}
