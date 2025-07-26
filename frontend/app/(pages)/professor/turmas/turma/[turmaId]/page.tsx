'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import styles from './page.module.css';

import Button from '../../../../../components/Button/Button';
import CardMateria from '../../../components/CardMateria/CardMateria';
import { ArrowLeft } from 'lucide-react';
import { InterfaceProfessor, InterfaceTurma, InterfaceMateria, InterfaceProfessorTurmaMateria } from '../../../../../types';
import { obterVinculosProfessorTurmaMateria } from '@/app/services/service_vinculos';
import { obterTurma } from '@/app/services/service_turma';
import { obterMateria } from '@/app/services/service_materia';

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
                handleGetMaterias(parsedProfessor.id);
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

    const handleGetMaterias = async (professor_id: string) => {
        try {
            // Busca as turmas-matérias que o professor leciona
            // Recebe uma lista de dicionários, onde cada dicionário contém 'professor_id', 'turma_id' e 'materia_id'
            const responseVinculos: InterfaceProfessorTurmaMateria[] = await obterVinculosProfessorTurmaMateria(professor_id);

            // Pega apenas os vínculos que tenham o ID da turma em questão
            const filteredVinculos = responseVinculos.filter(({ turma_id }) => turma_id === turmaId);

            // Pega apenas os IDs das matérias em cada vínculo
            const filteredMateriasIds = filteredVinculos.map(({ materia_id }) => materia_id);

            // Busca as matérias usando cada um dos IDs obtidos
            const responseMaterias: InterfaceMateria[] = await Promise.all(
                filteredMateriasIds.map(async (materia_id: string) => {
                    const responseMateria: InterfaceMateria = await obterMateria(materia_id);
                    return responseMateria;
                })
            );
            setMaterias(responseMaterias);
        }
        catch (error) {
            console.error("Erro ao buscar matérias:", error);
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
                    <p><strong>Semestre:</strong> {turma!.semestre}</p>
                    <p><strong>Turno:</strong> {turma!.turno.charAt(0).toUpperCase() + turma!.turno.slice(1)}</p>
                </div>
            </div>
            <div className={styles.materiasContainer}>
                <h2>Suas matérias nessa turma</h2>
                <div className={styles.listMaterias}>
                    {materias.map((materia) => (
                        <a href={`/professor/materias/materia/${turmaId}_${materia.id}`} key={materia.id}>
                            <CardMateria
                                key={materia.id}
                                materia={materia}
                                turma={turma!}
                            />
                        </a>
                    ))}
                </div>
            </div>
        </div>
    )
}
