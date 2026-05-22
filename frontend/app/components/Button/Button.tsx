import { ButtonHTMLAttributes } from 'react';
import styles from './Button.module.css';

type ButtonProps = Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'style'> & {
    style?: 'filled' | 'text' | 'ghost';
    size?: 'lg' | 'md' | 'sm';
    icon?: React.ReactNode;
    label: string;
    isDisabled?: boolean;
    action?: 'default' | 'primary' | 'secondary' | 'danger';
    fullWidth?: boolean;
};

export default function Button({
    style = 'text',
    size = 'md',
    icon,
    label,
    onClick,
    isDisabled,
    disabled,
    action = 'default',
    fullWidth = false,
    className,
    type = 'button',
    ...rest
}: ButtonProps) {
    const buttonClass = [
        styles.buttonContainer,
        style === 'filled' ? styles.filled : style === 'ghost' ? styles.ghost : styles.text,
        action === 'danger' ? styles.danger : '',
        action === 'primary' ? styles.primary : '',
        action === 'secondary' ? styles.secondary : '',
        size === 'lg' ? styles.sizeLg : size === 'sm' ? styles.sizeSm : '',
        fullWidth ? styles.fullWidth : '',
        className ?? '',
    ]
        .filter(Boolean)
        .join(' ');

    const buttonStateLayerClass = [
        styles.buttonStateLayer,
        icon ? styles.iconButton : '',
    ]
        .filter(Boolean)
        .join(' ');

    return (
        <button
            type={type}
            className={buttonClass}
            onClick={onClick}
            disabled={isDisabled ?? disabled}
            {...rest}
        >
            <div className={buttonStateLayerClass}>
                {icon}
                <span>{label}</span>
            </div>
        </button>
    );
}
