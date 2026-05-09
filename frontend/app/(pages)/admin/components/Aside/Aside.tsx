import { Home, BookOpen, ShieldUser, University, GraduationCap, FileText, Users, ChartColumn } from "lucide-react";
import styles from "./Aside.module.css"

export default function Aside(){
    return (
        <nav className={styles.navAside}>
            <section className={styles.sectionTitle}>
                <BookOpen/>
                <h1>Tutor</h1>
            </section>
            <section className={styles.sectionSubTitle}>
                <p>NAVEGAÇÃO</p>
            </section>
            <section className={styles.sectionLink}>
                <a href="/admin/"><section/><Home size={16}/>Painel</a>
                <a href="/admin/pages/administradores"><section/><ShieldUser size={16}/>Administradores</a>
                <a href="/admin/pages/professores"><section/><GraduationCap size={16}/>Professores</a>
                <a href="/admin/pages/alunos"><section/><Users size={16}/>Alunos</a>
                <a href="/admin/pages/materias"><section/><FileText size={16}/>Matérias</a>
                <a href="/admin/pages/turmas"><section/><University size={16}/>Turmas</a>
                <a href="/admin/pages/catalogoLLM"><section/><ChartColumn size={16}/>Catálogo de LLM</a>
            </section>
        </nav>
    )
}