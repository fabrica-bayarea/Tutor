'use client';

import styles from "./layout.module.css";
import { useAuth } from "@/contexts/AuthContext";

export default function AlunoLayout({ children }: { children: React.ReactNode }) {
    
    const { aluno, loading } = useAuth();

    if (loading) return null;

    if (!aluno) return null;

    return (
        <main className={styles.pageContainer}>
            {children}
        </main>
    );
}
