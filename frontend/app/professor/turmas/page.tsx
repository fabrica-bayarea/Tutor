'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';

import CardTurma from '../components/CardTurma/CardTurma';

import { InterfaceProfessor, InterfaceTurma } from '../../types';

export default function MinhasTurmas() {
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
            semestre: '20251',
            turno: 'Matutino'
        },
        {
            id: 'b3a5e72e-30d3-4c90-b3d4-0e3a06e3b65d',
            codigo: 'ADS01235',
            semestre: '20252',
            turno: 'Noturno'
        }
    ]);

    useEffect(() => {

    }, []);

    return (
        <div className={styles.midColumn}>
            <div className={styles.header}>
                <h1>Minhas turmas</h1>
                <p>Veja todas as turmas para as quais você leciona alguma matéria</p>
            </div>
            <div className={styles.listTurmas}>
                {turmas.map((turma) => (
                    <CardTurma key={turma.id} turma={turma} />
                ))}
            </div>
        </div>
    )
}
