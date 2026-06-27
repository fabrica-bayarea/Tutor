import styles from './ActionCard.module.css';

type ActionCardProps = {
    icon: React.ReactNode;
    title: string;
    description: string;
    onClick?: () => void;
    className?: string;
};

export default function ActionCard({ icon, title, description, onClick, className }: ActionCardProps) {
    return (
        <div
            className={[styles.card, className ?? ''].filter(Boolean).join(' ')}
            onClick={onClick}
            role={onClick ? 'button' : undefined}
            tabIndex={onClick ? 0 : undefined}
            onKeyDown={onClick ? (e) => e.key === 'Enter' && onClick() : undefined}
        >
            <span className={styles.icon}>{icon}</span>
            <div className={styles.content}>
                <p className={styles.title}>{title}</p>
                <p className={styles.description}>{description}</p>
            </div>
        </div>
    );
}
