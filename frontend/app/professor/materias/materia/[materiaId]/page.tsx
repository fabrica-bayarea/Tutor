'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import styles from './page.module.css';

import Button from '../../../../components/Button/Button';
import { InterfaceProfessor, InterfaceMateria, InterfaceTurma } from '../../../../types';
import { ArrowLeft, Plus } from 'lucide-react';

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
        <div className={styles.midColumn}>
            <div className={styles.header}>
                <Button
                    icon={<ArrowLeft size={24} />}
                    label="Voltar"
                    onClick={() => window.history.back()}
                />
                <h1>{turma.id}<br />{materia.id}</h1>
                <div className={styles.materiaInfo}>
                    <p><b>Turma:</b> {turma.codigo}</p>
                    <p><b>Código da matéria:</b> {materia.codigo}</p>
                </div>
            </div>
            <div className={styles.fontesAdicionadas}>
                <div className={styles.fontesAdicionadasHeader}>
                    <h2>Fontes adicionadas</h2>
                    <Button
                        style="filled"
                        icon={<Plus size={24} />}
                        label="Adicionar fonte"
                        onClick={() => { }}
                    />
                </div>
            </div>
        </div>
    )
}
