import styles from './CardTurma.module.css';

export default function CardTurma({
    turma: {
        id,
        codigo,
        semestre,
        turno
    }
}: {
    turma: {
        id: string;
        codigo: string;
        semestre: string;
        turno: string;
    }
}) {
    const turma = {
        id,
        codigo,
        semestre,
        turno
    }
    return (
        <div className={styles.cardTurma}>
            <div className={styles.cardTurmaStateLayer}>
                <h3 className={styles.cardTurmaCodigo}>{turma.codigo}</h3>
                <h4 className={styles.cardTurmaSemestreTurno}>{turma.semestre} - {turma.turno}</h4>
            </div>
        </div>
    )
}
