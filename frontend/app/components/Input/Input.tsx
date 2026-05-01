'use client';

import { forwardRef, InputHTMLAttributes, useId, useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import styles from './Input.module.css';

type InputProps = Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> & {
    label?: string;
    error?: string;
    helperText?: string;
    containerClassName?: string;
};

const Input = forwardRef<HTMLInputElement, InputProps>(function Input(
    {
        label,
        error,
        helperText,
        id,
        type = 'text',
        disabled,
        containerClassName,
        className,
        ...rest
    },
    ref
) {
    const generatedId = useId();
    const inputId = id ?? generatedId;
    const isPassword = type === 'password';
    const [revealed, setRevealed] = useState(false);
    const effectiveType = isPassword && revealed ? 'text' : type;

    return (
        <div className={`${styles.wrapper} ${containerClassName ?? ''}`}>
            {label && (
                <label htmlFor={inputId} className={styles.label}>
                    {label}
                </label>
            )}

            <div
                className={`${styles.field} ${error ? styles.fieldError : ''} ${
                    disabled ? styles.fieldDisabled : ''
                }`}
            >
                <input
                    ref={ref}
                    id={inputId}
                    type={effectiveType}
                    disabled={disabled}
                    aria-invalid={!!error}
                    aria-describedby={error || helperText ? `${inputId}-desc` : undefined}
                    className={`${styles.input} ${className ?? ''}`}
                    {...rest}
                />

                {isPassword && (
                    <button
                        type="button"
                        onClick={() => setRevealed((v) => !v)}
                        className={styles.toggleBtn}
                        tabIndex={-1}
                        aria-label={revealed ? 'Ocultar senha' : 'Mostrar senha'}
                        disabled={disabled}
                    >
                        {revealed ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                )}
            </div>

            {(error || helperText) && (
                <span
                    id={`${inputId}-desc`}
                    className={error ? styles.errorText : styles.helperText}
                >
                    {error ?? helperText}
                </span>
            )}
        </div>
    );
});

export default Input;
