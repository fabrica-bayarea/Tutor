'use client';

import React from "react";
import Aside from "./components/Aside/Aside";
import styles from "./layout.module.css";

export default function ProfessorLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <main className={styles.pageContainer}>
            <Aside />
            <div className={styles.midColumnContainer}>{children}</div>
        </main>
    );
}
