'use client';

import React, { useEffect, useState } from 'react';
import styles from './page.module.css';

import CardTurma from '../../components/CardTurma/CardTurma';

import { InterfaceUsuario, InterfaceTurma, InterfaceProfessorTurmaMateria } from '../../../../types';
import { obterVinculosProfessorTurmaMateria } from '@/app/services/service_vinculos';
import { obterTurma } from '@/app/services/service_turma';

export default function MinhasTurmas() {
    const [professor, setProfessor] = useState<InterfaceUsuario | null>(null);
    const [turmas, setTurmas] = useState<InterfaceTurma[]>([]);

    useEffect(() => {
        const professorData = localStorage.getItem("professor");
        if (professorData) {
            try {
                const parsedProfessor = JSON.parse(professorData);
                setProfessor(parsedProfessor);
                handleGetTurmas(parsedProfessor.id);
            } catch (error) {
                console.error("Erro ao fazer parse dos dados do professor:", error);
            }
        }
    }, []);

    const handleGetTurmas = async (professor_id: string) => {
            try {
                // Busca os vínculos do professor com turmas e matérias
                // Recebe uma lista de dicionários, onde cada dicionário contém 'professor_id', 'turma_id' e 'materia_id'
                const responseVinculos: InterfaceProfessorTurmaMateria[] = await obterVinculosProfessorTurmaMateria(professor_id);
    
                // Pega apenas os IDs das turmas em cada vínculo
                const filteredTurmasIds = responseVinculos.map(({ turma_id }) => turma_id);
    
                const responseTurmas: InterfaceTurma[] = await Promise.all(
                    filteredTurmasIds.map(async (turma_id: string) => {
                        const responseTurma: InterfaceTurma = await obterTurma(turma_id);
                        return responseTurma;
                    })
                );
                setTurmas(responseTurmas);
            } catch (error) {
                console.error('Erro ao buscar vínculos:', error);
            }
        };

    const mockTurma: InterfaceTurma = {
        id: 'dummy1',
        codigo: 'TURMA123',
        semestre: '2025.2',
        turno: 'Matutino'
        // preencha outros campos obrigatórios de InterfaceTurma se houver
    };

    return (
        <div className={styles.midColumn}>
            <div className={styles.header}>
                <h1>Minhas turmas</h1>
                <p>Veja todas as turmas para as quais você leciona alguma matéria</p>
            </div>
            <div className={styles.listTurmas}>
                {(turmas.length > 0 ? turmas : [mockTurma]).map((turma) => (
                    <a href={`/professor/turmas/turma/${turma.id}`} key={turma.id}>
                        <CardTurma turma={turma} />
                    </a>
                ))}
            </div>
        </div>
    )
}
