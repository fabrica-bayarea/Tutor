'use client';

import { useEffect, useState } from "react"
import styles from "./layout.module.css"
import { InterfaceUsuario } from "../../types"
import Aside from "./components/Aside/Aside";

export default function AlunoLayout({ children }: { children: React.ReactNode }) {
    const [aluno, setAluno] = useState<InterfaceUsuario | null>(null)

    useEffect(() => {
        const alunoData = localStorage.getItem("aluno")
        if (alunoData) {
            try {
                const parsed = JSON.parse(alunoData)
                setAluno(parsed)
            } catch (err) {
                console.error("Erro ao parsear aluno:", err)
            }
        }
    }, [])

    return (
        <section className={styles.mainSection}>
            <Aside/>
            <section className={styles.pageMediaSection}>
                {children}    
            </section>
        </section>
    )
}