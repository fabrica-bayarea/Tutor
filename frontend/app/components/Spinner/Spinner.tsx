import styles from './Spinner.module.css';

interface SpinnerProps {
    message?: string;
}

export default function Spinner({ message }: SpinnerProps) {
    return (
        <div className={styles.spinnerOverlay}>
            <div className={styles.spinner} />
            {message && <p className={styles.message}>{message}</p>}
        </div>
    );
}
