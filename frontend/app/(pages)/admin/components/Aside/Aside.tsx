'use client';

import { usePathname, useRouter } from 'next/navigation';
import { useContext } from 'react';
import { Home, ShieldUser, University, GraduationCap, FileText, Users, ChartColumn, X } from 'lucide-react';
import AsideMainButton from '../../../../components/AsideMainButton/AsideMainButton';
import TutorLogoIcon from '../../../../components/TutorLogoIcon';
import { LayoutContext } from '@/contexts/LayoutContext';
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
    const { isMenuMobileAberto, setIsMenuAbertoMobile } = useContext(LayoutContext)!;

    // No mobile, navegar fecha o drawer. No desktop a sidebar é fixa (CSS), então
    // o estado não interfere — fechar é inofensivo.
    function handleNavegar(href: string) {
        if (typeof window !== 'undefined' && window.innerWidth < 768) {
            setIsMenuAbertoMobile(false);
        }
        router.push(href);
    }

    return (
        <>
            {isMenuMobileAberto && (
                <div
                    className={styles.backdrop}
                    onClick={() => setIsMenuAbertoMobile(false)}
                    aria-hidden="true"
                />
            )}
            <nav className={isMenuMobileAberto ? styles.navAside : styles.navAsideHidden}>
                <section className={styles.sectionTopo}>
                    <section className={styles.sectionTitle}>
                        <TutorLogoIcon size={20} color="#0f766e" />
                        <h1>Tutor</h1>
                    </section>
                    <button
                        type="button"
                        className={styles.botaoFechar}
                        onClick={() => setIsMenuAbertoMobile(false)}
                        aria-label="Fechar menu"
                    >
                        <X size={20} color="#6b7280" />
                    </button>
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
                            onClick={() => handleNavegar(item.href)}
                        />
                    ))}
                </section>
            </nav>
        </>
    );
}
