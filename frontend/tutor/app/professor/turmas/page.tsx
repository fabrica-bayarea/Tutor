'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';

import Aside from '../components/Aside/Aside';

export default function MinhasTurmas() {
    return (
        <div className={styles.pageContainer}>
            <Aside selected="turmas" />
            <div className={styles.midColumn}>
                <div className={styles.header}>
                    <h1>Minhas Turmas</h1>
                    <p>Veja todas as turmas para as quais você leciona alguma matéria</p>
                </div>
                <div className={styles.listTurmas}></div>
            </div>
        </div>
    )
}
