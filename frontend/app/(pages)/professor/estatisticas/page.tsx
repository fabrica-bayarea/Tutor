'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';
import { ChartNoAxesCombined, ChartNoAxesColumnIncreasing, Shapes, Funnel} from 'lucide-react';
import { InterfaceProfessor } from '../../../types';
import BarraDeProgresso from '../components/BarraDeProgresso/BarraDeProgresso';
import Select from 'react-select';

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
                <div>
                    <h1>Estatísticas Completas</h1>
                    <p>Análise detalhada das dúvidas e engajamento.</p>
                </div>
                <div className={styles.filterButtons}>
                    <Funnel/>
                    <Select
                        isMulti
                        placeholder="Todas as matérias"
                        //options={options}
                        //onChange={handleVinculosChange}
                    />
                    <Select
                        isMulti
                        placeholder="Todas as Turmas"
                        //options={options}
                        //onChange={handleVinculosChange}
                    />
                </div>
            </div>

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

                <div className={styles.estatisticasRanking}>
                    <div className={styles.itemEstatisticaRanking}>
                        <div className={styles.headerEstatisticaRanking}>
                            <ChartNoAxesColumnIncreasing/>
                            <p className={styles.bolderText}>Ranking de dúvidas mais frequentes</p>
                        </div>
                        <div >
                            //foreach aqui
                            <div className={styles.itemRankeadoPerguntas}>
                                <div className={styles.perguntasInfos}>
                                    <p>Quais são as leis de Newton?</p>
                                    <p>Física</p>
                                </div>
                                <div className={styles.perguntasInfos}>
                                    <p className={styles.bolderText}>0</p>
                                    <p className={styles.legendBottomPercentage}>+0%</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className={styles.itemEstatisticaRanking}>
                        <div className={styles.headerEstatisticaRanking}>
                            <Shapes/>
                            <p className={styles.bolderText}>Distribuição por matéria</p>
                        </div>

                        <div>
                            //foreach aqui
                            <div className={styles.itemRankeadoVolume}>
                                <div className={styles.volumeInfos}>
                                    <p>Física</p>
                                    <p>0 dúvidas</p>
                                </div>
                                <BarraDeProgresso porcentagem={70} />
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    )
}
