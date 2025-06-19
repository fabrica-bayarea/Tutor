'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';

import Aside from '../components/Aside/Aside';
import CardMateria from '../components/CardMateria/CardMateria';

import { InterfaceProfessor, InterfaceMateria, InterfaceTurma, InterfaceTurmaMateria } from '../../types';

export default function MinhasMaterias() {
    const [professor, setProfessor] = useState<InterfaceProfessor>({
        id: '550e8400-e29b-41d4-a716-446655440000',
        matricula: '1',
        nome: 'Regiano',
        email: 'regiano@gmail.com',
        cpf: '12345678900' // ...senha, data_nascimento
    });
    const [turmas, setTurmas] = useState<InterfaceTurma[]>([
        {
            id: 'a4f98f1d-904c-4d8a-861e-df5a14c6e922',
            codigo: 'ADS01234',
            semestre: '2025/1',
            turno: 'matutino'
        },
        {
            id: 'b3a5e72e-30d3-4c90-b3d4-0e3a06e3b65d',
            codigo: 'ADS01235',
            semestre: '2025/2',
            turno: 'noturno'
        }
    ]);
    const [materias, setMaterias] = useState<InterfaceMateria[]>([
        {
            id: '3f8a1f0b-5d5c-4a37-bb1d-03f057349b15',
            codigo: 'ADS001',
            nome: 'Banco de Dados'
        },
        {
            id: '8b14cd22-d2f3-4621-99d9-58764f28db45',
            codigo: 'ADS002',
            nome: 'Lógica de Programação'
        },
        {
            id: '6d7c5ed7-c78f-44cb-bad9-5f4d3f131417',
            codigo: 'ADS003',
            nome: 'Auditoria e Segurança de Software'
        }
    ]);
    const [turmasMaterias, setTurmasMaterias] = useState<InterfaceTurmaMateria[]>([
        {
            turma_id: 'a4f98f1d-904c-4d8a-861e-df5a14c6e922',
            materia_id: '3f8a1f0b-5d5c-4a37-bb1d-03f057349b15'
        },
        {
            turma_id: 'a4f98f1d-904c-4d8a-861e-df5a14c6e922',
            materia_id: '8b14cd22-d2f3-4621-99d9-58764f28db45'
        },
        {
            turma_id: 'b3a5e72e-30d3-4c90-b3d4-0e3a06e3b65d',
            materia_id: '6d7c5ed7-c78f-44cb-bad9-5f4d3f131417'
        },
        {
            turma_id: 'b3a5e72e-30d3-4c90-b3d4-0e3a06e3b65d',
            materia_id: '8b14cd22-d2f3-4621-99d9-58764f28db45'
        }
    ]);
    
    useEffect(() => {
        
    }, []);

    return (
        <div className={styles.pageContainer}>
            <Aside selected="materias" />
            <div className={styles.midColumn}>
                <div className={styles.header}>
                    <h1>Minhas matérias</h1>
                    <p>Veja todas as matérias que você leciona</p>
                </div>
                <div className={styles.listMaterias}>
                    {materias.map((materia) => (
                        <a href={`/professor/materias/materia/${turmasMaterias.find((turmaMateria) => turmaMateria.materia_id === materia.id)?.turma_id}_${materia.id}`} key={materia.id}>
                            <CardMateria key={materia.id} materia={materia} turma={turmas.find((turma) => turma.id === turmasMaterias.find((turmaMateria) => turmaMateria.materia_id === materia.id)?.turma_id)!} />
                        </a>
                    ))}
                </div>
            </div>
        </div>
    )
}
