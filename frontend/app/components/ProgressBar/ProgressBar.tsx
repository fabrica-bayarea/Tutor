import styles from './ProgressBar.module.css';

type ProgressBarProps = {
    value: number;
    color?: string;
    height?: number;
    className?: string;
};

export default function ProgressBar({
    value,
    color = '#0d9488',
    height = 12,
    className,
}: ProgressBarProps) {
    const clamped = Math.min(100, Math.max(0, value));

    return (
        <div
            className={[styles.track, className ?? ''].filter(Boolean).join(' ')}
            style={{ height }}
            role="progressbar"
            aria-valuenow={clamped}
            aria-valuemin={0}
            aria-valuemax={100}
        >
            <div
                className={styles.fill}
                style={{ width: `${clamped}%`, backgroundColor: color, height }}
            />
        </div>
    );
}
