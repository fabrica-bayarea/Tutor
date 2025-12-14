'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';
import { ChartNoAxesCombined, ChartNoAxesColumnIncreasing, Shapes, Funnel, Car} from 'lucide-react';
import { InterfaceUsuario } from '../../../types';
import BarraDeProgresso from '../components/BarraDeProgresso/BarraDeProgresso';
import Select from 'react-select';
import CardPequeno from '../components/CardPequeno/CardPequeno';
import CardMedio from '../components/CardMedio/CardMedio';

export default function Home() {
    const [professor, setProfessor] = useState<InterfaceUsuario>({
        id: '550e8400-e29b-41d4-a716-446655440000',
        matricula: '1',
        nome: 'Regiano',
        email: 'regiano@gmail.com',
        role: '2'
    });
    
    useEffect(() => {
        
    }, []);
    
    return (
        <div className={styles.midColumn}>
            <div className={styles.header}>
                <div>
                    <h1>Estatísticas Completas</h1>
                    <p>Análise detalhada das dúvidas e engajamento.</p>
                </div>
                <div className={styles.filterButtons}>
                    <Funnel/>
                    <Select
                        instanceId="materia-select"
                        isMulti
                        placeholder="Todas as matérias"
                        //options={options}
                        //onChange={handleVinculosChange}
                    />
                    <Select
                        instanceId="materia-select"
                        isMulti
                        placeholder="Todas as Turmas"
                        //options={options}
                        //onChange={handleVinculosChange}
                    />
                </div>
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
                        titulo='Tempo médio de uso' 
                        volume='0hr'
                        porcentagem='0'
                        tempo='este mês'
                    />
                </div>

                <div className={styles.itensEstatisticosTelaPrincipal}>
                    <CardMedio
                        titulo = 'Ranking de dúvidas mais frequentes'
                        tipo = 'RankingDeDuvidas'
                        itens = {[
                            { 
                                duvida: 'Quais são as leis de Newton?', 
                                materia: 'Física', 
                                volume: '0', 
                                porcentagem: '+0'
                            },
                            { 
                                duvida: 'Quanto é um mais um?', 
                                materia: 'Matemática', 
                                volume: '0', 
                                porcentagem: '+0'
                            },
                        ]}
                    />
                    <CardMedio
                        titulo = 'Distribuição por matéria'
                        tipo = 'RankingDeMaterias'
                        itens = {[
                            { 
                                duvida: '', 
                                materia: 'Física', 
                                volume: '1', 
                                porcentagem: '50'
                            },
                            { 
                                duvida: '', 
                                materia: 'Matemática', 
                                volume: '1', 
                                porcentagem: '50'
                            },
                        ]}
                    />
                </div>

            </div>
        </div>
    )
}
