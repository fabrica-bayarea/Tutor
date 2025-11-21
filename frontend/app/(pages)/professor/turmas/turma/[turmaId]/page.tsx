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
import { ChartNoAxesCombined} from 'lucide-react';

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
        </div>
    )
}
