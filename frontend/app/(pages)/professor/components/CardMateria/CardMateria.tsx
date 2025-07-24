import styles from './CardMateria.module.css';
import { InterfaceMateria, InterfaceTurma } from '../../../../types';

export default function CardMateria({
    materia: {
        id: materia_id,
        codigo: materia_codigo,
        nome: materia_nome,
    },
    turma: {
        id: turma_id,
        codigo: turma_codigo,
        semestre: turma_semestre,
        turno: turma_turno
    }
}: {
    materia: InterfaceMateria,
    turma: InterfaceTurma
}) {
    const materia = {
        id: materia_id,
        codigo: materia_codigo,
        nome: materia_nome,
    }
    
    const turma = {
        id: turma_id,
        codigo: turma_codigo,
        semestre: turma_semestre,
        turno: turma_turno
    }
    
    return (
        <div className={styles.cardMateria}>
            <div className={styles.cardMateriaStateLayer}>
                <h3 className={styles.cardMateriaNome}>{materia.nome}</h3>
                <h4 className={styles.cardMateriaTurmaCodigo}>{turma.codigo} - {materia.codigo}</h4>
            </div>
        </div>
    )
}
