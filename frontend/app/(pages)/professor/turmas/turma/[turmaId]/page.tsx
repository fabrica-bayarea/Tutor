'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import styles from './page.module.css';

import Button from '../../../../../components/Button/Button';
import CardMateria from '../../../components/CardMateria/CardMateria';
import { ArrowLeft, ChartNoAxesCombined, ChartNoAxesColumnIncreasing, Brain, GraduationCap, ChevronRight } from 'lucide-react';
import { InterfaceProfessor, InterfaceTurma, InterfaceMateria, InterfaceProfessorTurmaMateria } from '../../../../../types';
import { obterVinculosProfessorTurmaMateria } from '@/app/services/service_vinculos';
import { obterTurma } from '@/app/services/service_turma';
import { obterMateria } from '@/app/services/service_materia';
import BarraDeProgresso from '../../../components/BarraDeProgresso/BarraDeProgresso';

export default function Turma() {
    const params = useParams();
    const [professor, setProfessor] = useState<InterfaceProfessor | null>(null);
    const turmaId = params.turmaId as string;

    const [turma, setTurma] = useState<InterfaceTurma | null>({
        id: turmaId,
        codigo: '',
        semestre: '',
        turno: ''
    });
    const [materias, setMaterias] = useState<InterfaceMateria[]>([]);
    const [vinculos, setVinculos] = useState<InterfaceProfessorTurmaMateria[] | null>(null); 

    useEffect(() => {
        const professorData = localStorage.getItem("professor");
        if (professorData) {
            try {
                const parsedProfessor: InterfaceProfessor = JSON.parse(professorData);
                setProfessor(parsedProfessor);
                handleGetTurma(turmaId);
            } catch (error) {
                console.error("Erro ao fazer parse dos dados do professor:", error);
            }
        }
    }, []);

    const handleGetTurma = async (turma_id: string) => {
        try {
            const turmaData: InterfaceTurma = await obterTurma(turma_id);
            setTurma(turmaData);
        } catch (error) {
            console.error("Erro ao buscar turma:", error);
        }
    }

    return (
        <div className={styles.midColumn}>
            <div className={styles.header}>
                <Button
                    icon={<ArrowLeft size={24} />}
                    label="Voltar"
                    onClick={() => window.history.back()}
                />
                <h1>{turma?.codigo}</h1>
                <div className={styles.turmaInfo}>
                    <h1>{turma!.codigo}</h1>
                    <p><strong>Semestre:</strong> {turma!.semestre}</p>
                    <p><strong>Turno:</strong> {turma!.turno.charAt(0).toUpperCase() + turma!.turno.slice(1)}</p>
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
                    <div className={styles.itemDireito}>
                        <div className={styles.itemEstatisticaRanking}>
                            <div className={styles.headerEstatisticaRanking}>
                                <Brain/>
                                <p className={styles.bolderText}>Insights do Tutor</p>
                            </div>

                            <div>
                                <p>
                                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Ducimus dicta sit quia assumenda inventore, 
                                    porro eius qui atque ratione blanditiis earum sint illo consectetur incidunt! Quo explicabo quidem 
                                    eveniet dolore.
                                </p>
                            </div>
                        </div>
                        <div className={styles.itemEstatisticaRanking}>
                            <div className={styles.headerEstatisticaRanking}>
                                <GraduationCap/>
                                <p className={styles.bolderText}>Matérias ensinadas</p>
                            </div>

                            <div>
                                //foreach aqui
                                <div className={styles.itemRankeadoVolume}>
                                    <div className={styles.itemDireitoMateria}>
                                        <p>Física</p>
                                        <ChevronRight/>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className={styles.itemA}>
                            <a href="/professor/estatisticas" className={styles.buttonA}>
                                <button className={styles.buttonEst}>Ver Estatísticas Completas</button>
                            </a>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    )
}
