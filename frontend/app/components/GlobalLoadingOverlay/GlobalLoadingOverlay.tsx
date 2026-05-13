'use client';

import { useEffect, useState } from 'react';
import { loadingEmitter } from '@/app/services/loadingEmitter';
import styles from './GlobalLoadingOverlay.module.css';

export default function GlobalLoadingOverlay() {
    const [active, setActive] = useState(false);

    useEffect(() => {
        loadingEmitter.register(setActive);
    }, []);

    if (!active) return null;

    return (
        <div className={styles.overlay}>
            <div className={styles.spinner} />
        </div>
    );
}
