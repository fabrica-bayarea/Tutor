'use client';

import { useEffect } from 'react';
import { X } from 'lucide-react';
import styles from './Toast.module.css';

type ToastType = 'error' | 'success' | 'info';

type ToastProps = {
    message: string;
    type?: ToastType;
    duration?: number;
    onClose: () => void;
};

export default function Toast({
    message,
    type = 'error',
    duration = 5000,
    onClose,
}: ToastProps) {
    useEffect(() => {
        if (duration <= 0) return;
        const timer = setTimeout(onClose, duration);
        return () => clearTimeout(timer);
    }, [duration, onClose]);

    return (
        <div className={`${styles.toast} ${styles[type]}`} role="alert" aria-live="polite">
            <button
                type="button"
                onClick={onClose}
                className={styles.closeBtn}
                aria-label="Fechar"
            >
                <X size={16} strokeWidth={2.4} />
            </button>
            <span className={styles.message}>{message}</span>
        </div>
    );
}
