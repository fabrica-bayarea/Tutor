'use client';

import { useEffect } from 'react';
import { Check, X, Info } from 'lucide-react';
import styles from './Toast.module.css';

type ToastType = 'error' | 'success' | 'info';

type ToastProps = {
    message: string;
    type?: ToastType;
    duration?: number;
    icon?: React.ReactNode;
    onClose: () => void;
    standalone?: boolean; // false = sem position:fixed (usado no ToastContainer)
};

const defaultIcons: Record<ToastType, React.ReactNode> = {
    success: <Check size={18} strokeWidth={2.5} color="white" />,
    error: <X size={18} strokeWidth={2.5} color="white" />,
    info: <Info size={18} strokeWidth={2} color="white" />,
};

export default function Toast({
    message,
    type = 'error',
    duration = 5000,
    icon,
    onClose,
    standalone = true,
}: ToastProps) {
    useEffect(() => {
        if (duration <= 0) return;
        const timer = setTimeout(onClose, duration);
        return () => clearTimeout(timer);
    }, [duration, onClose]);

    return (
        <div
            className={`${styles.toast} ${styles[type]} ${standalone ? '' : styles.inline}`}
            role="alert"
            aria-live="polite"
        >
            <span className={styles.icon}>{icon ?? defaultIcons[type]}</span>
            <span className={styles.message}>{message}</span>
        </div>
    );
}
