import styles from './Button.module.css';

interface ButtonProps {
    style?: 'filled' | 'text';
    icon?: React.ReactNode;
    label: string;
    isDisabled?: boolean;
    action?: 'default' | 'danger';
    onClick?: () => void;
    props?: React.ButtonHTMLAttributes<HTMLButtonElement>
}

export default function Button({
    style = 'text',
    icon,
    label,
    onClick,
    isDisabled,
    action = 'default',
    ...props
}: ButtonProps) {
    const buttonClass = `
        ${styles.buttonContainer}
        ${style === 'filled' ? styles.filled : styles.text}
        ${action === 'danger' ? styles.danger : ''}
    `.trim();

    const buttonStateLayerClass = `
        ${styles.buttonStateLayer}
        ${icon ? styles.iconButton : ''}
    `.trim();

    return (
        <button
            className={buttonClass}
            onClick={onClick}
            disabled={isDisabled}
            {...props}
        >
            <div className={buttonStateLayerClass}>
                {icon}
                <span>{label}</span>
            </div>
        </button>
    );
}
