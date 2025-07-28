'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';

import CardMateria from '../components/CardMateria/CardMateria';

import { InterfaceProfessor, InterfaceMateria, InterfaceTurma, InterfaceTurmaMateria, InterfaceProfessorTurmaMateria } from '../../../types';
import { obterVinculosProfessorTurmaMateria } from '@/app/services/service_vinculos';
import { obterTurma } from '@/app/services/service_turma';
import { obterMateria } from '@/app/services/service_materia';

export default function MinhasMaterias() {
    const [professor, setProfessor] = useState<InterfaceProfessor | null>(null);
    const [turmas, setTurmas] = useState<InterfaceTurma[]>([]);
    const [materias, setMaterias] = useState<InterfaceMateria[]>([]);
    const [turmasMaterias, setTurmasMaterias] = useState<InterfaceTurmaMateria[]>([]);

    useEffect(() => {
        const professorData = localStorage.getItem("professor");
        if (professorData) {
            try {
                const parsedProfessor: InterfaceProfessor = JSON.parse(professorData);
                setProfessor(parsedProfessor);
                handleGetMaterias(parsedProfessor.id);
            } catch (error) {
                console.error("Erro ao fazer parse dos dados do professor:", error);
            }
        }
    }, []);

    const handleGetMaterias = async (professor_id: string) => {
        try {
            // Busca as turmas-matérias que o professor leciona
            // Recebe uma lista de dicionários, onde cada dicionário contém 'professor_id', 'turma_id' e 'materia_id'
            const responseVinculos: InterfaceProfessorTurmaMateria[] = await obterVinculosProfessorTurmaMateria(professor_id);
            console.log(`Vínculos: ${JSON.stringify(responseVinculos, null, 2)}`);

            const filteredVinculos = responseVinculos.map(vinculo => {
                const { turma_id, materia_id } = vinculo;
                return { turma_id, materia_id };
            })
            // Pega apenas os IDs das turmas em cada vínculo
            const filteredTurmasIds = filteredVinculos.map(({ turma_id }) => turma_id);
            // Remove IDs duplicados
            const uniqueTurmaIds = [...new Set(filteredTurmasIds)];

            // Pega apenas os IDs das matérias em cada vínculo
            const filteredMateriasIds = filteredVinculos.map(({ materia_id }) => materia_id);
            // Remove IDs duplicados
            const uniqueMateriaIds = [...new Set(filteredMateriasIds)];

            // Busca as turmas usando cada um dos IDs obtidos
            const responseTurmas: InterfaceTurma[] = await Promise.all(
                uniqueTurmaIds.map(
                    async (turma_id: string) => await obterTurma(turma_id)
                )
            );
            console.log(`Turmas: ${JSON.stringify(responseTurmas, null, 2)}`);
            // Busca as matérias usando cada um dos IDs obtidos
            const responseMaterias: InterfaceMateria[] = await Promise.all(
                uniqueMateriaIds.map(
                    async (materia_id: string) => await obterMateria(materia_id)
                )
            );
            console.log(`Materias: ${JSON.stringify(responseMaterias, null, 2)}`);

            setTurmas(responseTurmas);
            setMaterias(responseMaterias);
            setTurmasMaterias(filteredVinculos);
        } catch (error) {
            console.error("Erro ao obter as matérias:", error);
        }
    }

    return (
        <div className={styles.midColumn}>
            <div className={styles.header}>
                <h1>Minhas matérias</h1>
                <p>Veja todas as matérias que você leciona</p>
            </div>
            <div className={styles.listMaterias}>
                {turmasMaterias.map((turmaMateria) => (
                    <a href={`/professor/materias/materia/${turmaMateria.turma_id}_${turmaMateria.materia_id}`} key={`${turmaMateria.turma_id}_${turmaMateria.materia_id}`}>
                        <CardMateria
                            materia={materias.find((materia) => materia.id === turmaMateria.materia_id)!}
                            turma={turmas.find((turma) => turma.id === turmaMateria.turma_id)!}
                        />
                    </a>
                ))}
            </div>
        </div>
    )
}
