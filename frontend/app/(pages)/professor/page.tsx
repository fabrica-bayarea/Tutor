'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';
import { ChartNoAxesCombined } from 'lucide-react';
import { InterfaceProfessor } from '../../types';
import CardPequeno from './components/CardPequeno/CardPequeno';
import UserButton from './components/UserButton/userButton';

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
            <div className={styles.itensTelaPrincipal}>
                <div className={styles.itensEstatisticosTelaPrincipal}>
                    <CardPequeno
                        titulo='Total de dúvidas' 
                        volume='0'
                        porcentagem='0'
                        tempo='este mês'
                    />
                    <CardPequeno
                        titulo='Alunos Ativos' 
                        volume='0'
                        porcentagem='0'
                        tempo='este mês'
                    />
                    <CardPequeno
                        titulo='Tempo médio de uso' 
                        volume='0hr'
                        porcentagem='0'
                        tempo='este mês'
                    />
                    <CardPequeno
                        titulo='Total de dúvidas' 
                        volume='0'
                        porcentagem='0'
                        tempo='este mês'
                    />
                </div>

                <div className={styles.itensAcoesRapidasTelaPrincipal}>
                    <div className={styles.itemAcoesRapidasTelaPrincipal}>
                        <p className={styles.bolderText}>Ações rápidas</p>
                        <a href="/professor/estatisticas">
                            <button className={styles.buttonAcoesRapidas}>Ver Estatísticas Completas</button>
                        </a>
                        <a href="/professor/upload">
                            <button className={styles.buttonAcoesRapidas}>Adicionar Conteúdo</button>
                        </a>
                        <a href="/professor/config">
                            <button className={styles.buttonConfig}>Configurações</button>
                        </a>
                    </div>
                    <div className={styles.itemAcoesRapidasTelaPrincipal}>
                        <p className={styles.bolderText}>Tutor AI</p>
                        <a href="/professor/chat" >
                            <button className={styles.buttonAcoesRapidas}>Abrir chat Tutor</button>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    )
}
