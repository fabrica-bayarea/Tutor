import styles from './BarraDeProgresso.module.css';

export default function BarraDeProgresso({ porcentagem = 0 }) {
    return (
        <div className={styles.bar}>
            <div className={styles.fill} style={{ width: `${porcentagem}%` }}/>
        </div>
    );
}