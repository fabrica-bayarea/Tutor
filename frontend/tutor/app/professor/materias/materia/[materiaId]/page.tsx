'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';

import Aside from '../../../components/Aside/Aside';
import { useParams } from 'next/navigation';
import { InterfaceProfessor, InterfaceMateria, InterfaceTurma } from '../../../../types';

export default function Home() {
    const params = useParams();
    const [turmaId, materiaId] = (params.materiaId as string).split('_');

    const [professor, setProfessor] = useState<InterfaceProfessor>({
        id: '550e8400-e29b-41d4-a716-446655440000',
        matricula: '1',
        nome: 'Regiano',
        email: 'regiano@gmail.com',
        cpf: '12345678900' // ...senha, data_nascimento
    });
    const [turma, setTurma] = useState<InterfaceTurma>({
        id: turmaId,
        codigo: '',
        semestre: '',
        turno: ''
    });
    const [materia, setMateria] = useState<InterfaceMateria>({
        id: materiaId,
        codigo: '',
        nome: ''
    });
    
    useEffect(() => {
        
    }, []);
    
    return (
        <div className={styles.pageContainer}>
            <Aside selected='materias' />
            <div className={styles.midColumn}>
                <div className={styles.header}>
                    <h1>{turma.id}<br />{materia.id}</h1>
                </div>
            </div>
        </div>
    )
}
