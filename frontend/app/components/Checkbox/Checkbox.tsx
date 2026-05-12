import { useId } from 'react';
import styles from './Checkbox.module.css';

type CheckboxProps = {
    checked: boolean;
    onChange: (checked: boolean) => void;
    label?: string;
    disabled?: boolean;
    id?: string;
    className?: string;
};

export default function Checkbox({ checked, onChange, label, disabled, id, className }: CheckboxProps) {
    const generatedId = useId();
    const inputId = id ?? generatedId;

    return (
        <label
            htmlFor={inputId}
            className={[styles.wrapper, disabled ? styles.disabled : '', className ?? ''].filter(Boolean).join(' ')}
        >
            <span className={[styles.box, checked ? styles.checked : ''].filter(Boolean).join(' ')}>
                <input
                    id={inputId}
                    type="checkbox"
                    checked={checked}
                    disabled={disabled}
                    onChange={(e) => onChange(e.target.checked)}
                    className={styles.input}
                />
                {checked && (
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
                        <path d="M2 7L5.5 10.5L12 4" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                )}
            </span>
            {label && <span className={styles.label}>{label}</span>}
        </label>
    );
}
