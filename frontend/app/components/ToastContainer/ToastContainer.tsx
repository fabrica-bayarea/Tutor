'use client';

import { useEffect } from 'react';
import { useToast } from '@/contexts/ToastContext';
import { toastEmitter } from '@/app/services/toastEmitter';
import Toast from '../Toast/Toast';
import styles from './ToastContainer.module.css';

export default function ToastContainer() {
    const { toasts, addToast, removeToast } = useToast();

    useEffect(() => {
        toastEmitter.register(addToast);
    }, [addToast]);

    if (toasts.length === 0) return null;

    return (
        <div className={styles.container}>
            {toasts.map((t) => (
                <Toast
                    key={t.id}
                    message={t.message}
                    type={t.type}
                    duration={t.duration}
                    onClose={() => removeToast(t.id)}
                    standalone={false}
                />
            ))}
        </div>
    );
}
