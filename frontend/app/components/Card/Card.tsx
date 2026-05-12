import styles from './Card.module.css';

type CardProps = {
    variant?: 'default' | 'brand' | 'warning' | 'danger' | 'success';
    title?: string;
    children: React.ReactNode;
    className?: string;
};

export default function Card({ variant = 'default', title, children, className }: CardProps) {
    return (
        <div className={[styles.card, styles[variant], className ?? ''].filter(Boolean).join(' ')}>
            <div className={styles.accent} />
            {title && <p className={styles.title}>{title}</p>}
            <div className={styles.content}>{children}</div>
        </div>
    );
}
