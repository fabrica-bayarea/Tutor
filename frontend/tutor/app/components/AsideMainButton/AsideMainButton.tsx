import styles from './AsideMainButton.module.css';

export default function AsideMainButton({
    icon,
    label,
    isCollapsed,
    isSelected,
    ...props
}: {
    icon: React.ReactNode;
    label: string;
    isCollapsed: boolean;
    isSelected?: boolean;
} & React.ButtonHTMLAttributes<HTMLButtonElement>) {
    return (
        <button
            className={styles.asideMainButton}
            {...props}
        >
            <div className={`${styles.asideMainButtonStateLayer} ${isCollapsed ? styles.collapsed : styles.expanded} ${isSelected ? styles.selected : ''}`}>
                {icon}
                <span className={styles.asideMainButtonLabel}>
                    {isCollapsed ? '' : label}
                </span>
            </div>
        </button>
    );
}
