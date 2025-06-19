import styles from './IconButton.module.css';

interface IconButtonProps {
    icon: React.ReactNode;
    title?: string;
}

export default function IconButton({
    icon,
    title,
    ...props
}: IconButtonProps & React.ButtonHTMLAttributes<HTMLButtonElement>) {
    return (
        <button
            className={styles.iconButton}
            title={title}
            {...props}
        >
            <div className={styles.iconButtonStateLayer}>
                {icon}
            </div>
        </button>
    );
}
