import styles from './CardPequeno.module.css';
import { ChartNoAxesCombined } from 'lucide-react';

export default function CardPequeno({ titulo = '', volume = '', porcentagem = '', tempo = ''}) {
    return (
        <div className={styles.itemEstatisticoTelaPrincipal}>
            <div className={styles.itemEstatistico}>
                <p>{`${titulo}`}</p>
            </div>
            <div className={styles.itemEstatistico}>
                <p className={styles.bolderText}>{`${volume}`}</p>
            </div>
            <div className={styles.legenda}>
                <ChartNoAxesCombined/>
                <p className={styles.legendBottomPercentage}>{`${porcentagem}`}%</p>
                <p className={styles.legendBottom}>{` ${tempo}`}</p>
            </div>
        </div>
    );
}