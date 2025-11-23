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
import CardPequeno from '../../../components/CardPequeno/CardPequeno';
import CardMedio from '../../../components/CardMedio/CardMedio';

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
                </div>

                <div className={styles.estatisticasRanking}>
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

                    <div className={styles.itemDireito}>
                        <CardMedio
                            titulo = 'Ranking de dúvidas mais frequentes'
                            tipo = 'InsightTutor'
                            itens = {[]}
                        />
                        <CardMedio
                            titulo = 'Ranking de dúvidas mais frequentes'
                            tipo = 'MateriasEnsinadas'
                            itens = {[
                                { 
                                    duvida: '', 
                                    materia: 'Física', 
                                    volume: '', 
                                    porcentagem: ''
                                },
                                { 
                                    duvida: '', 
                                    materia: 'Matemática', 
                                    volume: '', 
                                    porcentagem: ''
                                }
                            ]}
                        />
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
