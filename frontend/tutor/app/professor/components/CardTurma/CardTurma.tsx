import styles from './CardTurma.module.css';

export default function CardTurma({
    codigo_turma,
    semestre_turma,
    turno_turma
}: {
    codigo_turma: string;
    semestre_turma: string;
    turno_turma: string;
}) {
    const turma = {
        codigo: codigo_turma,
        semestre: semestre_turma,
        turno: turno_turma
    }
    return (
        <div className={styles.cardTurma}>
            <div className={styles.cardTurmaStateLayer}>
                <h2>{turma.codigo}</h2>
                <h3>{turma.semestre} - {turma.turno}</h3>
            </div>
        </div>
    )
}
