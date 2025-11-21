'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';
import { ChartNoAxesCombined } from 'lucide-react';
import { InterfaceProfessor } from '../../types';

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

                <div className={styles.itensTelaPrincipal}>
                    <div className={styles.itensEstatisticosTelaPrincipal}>
                        <div className={styles.itemEstatisticoTelaPrincipal}>
                            <div className={styles.itemEstatistico}>
                                <p>Total de  Dúvidas</p>
                            </div>
                            <div className={styles.itemEstatistico}>
                                <p className={styles.bolderText}>0</p>
                            </div>
                            <div className={styles.legenda}>
                                <ChartNoAxesCombined/>
                                <p className={styles.legendBottomPercentage}>+0% </p>
                                <p className={styles.legendBottom}> este mês</p>
                            </div>
                        </div>
                        <div className={styles.itemEstatisticoTelaPrincipal}>
                            <div className={styles.itemEstatistico}>
                                <p>Alunos Ativos</p>
                            </div>
                            <div className={styles.itemEstatistico}>
                                <p className={styles.bolderText}>0</p>
                            </div>
                            <div className={styles.legenda}>
                                <ChartNoAxesCombined/>
                                <p className={styles.legendBottomPercentage}>+0% </p>
                                <p className={styles.legendBottom}> este mês</p>
                            </div>
                        </div>
                        <div className={styles.itemEstatisticoTelaPrincipal}>
                            <div className={styles.itemEstatistico}>
                                <p>Tempo médio de uso</p>
                            </div>
                            <div className={styles.itemEstatistico}>
                                <p className={styles.bolderText}>0hr</p>
                            </div>
                            <div className={styles.legenda}>
                                <ChartNoAxesCombined/>
                                <p className={styles.legendBottomPercentage}>+0% </p>
                                <p className={styles.legendBottom}> este mês</p>
                            </div>
                        </div>
                        <div className={styles.itemEstatisticoTelaPrincipal}>
                            <div className={styles.itemEstatistico}>
                                <p>Total de dúvidas</p>
                            </div>
                            <div className={styles.itemEstatistico}>
                                <p className={styles.bolderText}>0</p>
                            </div>
                            <div className={styles.legenda}>
                                <ChartNoAxesCombined/>
                                <p className={styles.legendBottomPercentage}>+0% </p>
                                <p className={styles.legendBottom}> este mês</p>
                            </div>
                        </div>
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
        </div>
    )
}
