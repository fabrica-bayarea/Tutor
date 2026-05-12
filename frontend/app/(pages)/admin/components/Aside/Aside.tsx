'use client';

import { usePathname, useRouter } from 'next/navigation';
import { Home, BookOpen, ShieldUser, University, GraduationCap, FileText, Users, ChartColumn } from 'lucide-react';
import AsideMainButton from '../../../../components/AsideMainButton/AsideMainButton';
import styles from './Aside.module.css';

const navItems = [
    { label: 'Painel',           icon: <Home size={16} />,         href: '/admin',                        match: (p: string) => p === '/admin' || p === '/admin/' },
    { label: 'Administradores',  icon: <ShieldUser size={16} />,   href: '/admin/pages/administradores',  match: (p: string) => p.startsWith('/admin/pages/administradores') },
    { label: 'Professores',      icon: <GraduationCap size={16} />,href: '/admin/pages/professores',      match: (p: string) => p.startsWith('/admin/pages/professores') },
    { label: 'Alunos',           icon: <Users size={16} />,        href: '/admin/pages/alunos',           match: (p: string) => p.startsWith('/admin/pages/alunos') },
    { label: 'Matérias',         icon: <FileText size={16} />,     href: '/admin/pages/materias',         match: (p: string) => p.startsWith('/admin/pages/materias') },
    { label: 'Turmas',           icon: <University size={16} />,   href: '/admin/pages/turmas',           match: (p: string) => p.startsWith('/admin/pages/turmas') },
    { label: 'Catálogo de LLM',  icon: <ChartColumn size={16} />,  href: '/admin/pages/catalogoLLM',      match: (p: string) => p.startsWith('/admin/pages/catalogoLLM') },
];

export default function Aside() {
    const pathname = usePathname();
    const router = useRouter();

    return (
        <nav className={styles.navAside}>
            <section className={styles.sectionTitle}>
                <BookOpen size={20} color="#0d9488" />
                <h1>Tutor</h1>
            </section>
            <section className={styles.sectionSubTitle}>
                <p>NAVEGAÇÃO</p>
            </section>
            <section className={styles.sectionLink}>
                {navItems.map((item) => (
                    <AsideMainButton
                        key={item.href}
                        icon={item.icon}
                        label={item.label}
                        isSelected={item.match(pathname ?? '')}
                        onClick={() => router.push(item.href)}
                    />
                ))}
            </section>
        </nav>
    );
}
