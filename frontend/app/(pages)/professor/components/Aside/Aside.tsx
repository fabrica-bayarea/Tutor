'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import styles from './Aside.module.css';
import { Menu, House, GraduationCap, LibraryBig, Plus } from 'lucide-react';
import AsideMainButton from '../../../../components/AsideMainButton/AsideMainButton';

export default function Aside() {
    const pathname = usePathname();

    const getSelected = () => {
        if (pathname.endsWith('/professor')) return 'home';
        if (pathname.includes('/professor/turmas')) return 'turmas';
        if (pathname.includes('/professor/materias')) return 'materias';
        if (pathname.includes('/professor/upload')) return 'addFontes';
        return null;
    };

    const selectedSection = getSelected();

    useEffect(() => {

    }, []);

    return (
        <div className={styles.asideContainer}>
            <div className={styles.asideHeader}>
                <img src="null" alt="" />
            </div>
            <div className={styles.asideMainButtons}>
                <a href="/professor">
                    <AsideMainButton
                        icon={<House />}
                        label="Início"
                        isCollapsed={false}
                        isSelected={selectedSection === 'home'}
                    />
                </a>
                <a href="/professor/turmas">
                    <AsideMainButton
                        icon={<GraduationCap />}
                        label="Minhas turmas"
                        isCollapsed={false}
                        isSelected={selectedSection === 'turmas'}
                    />
                </a>
                <a href="/professor/materias">
                    <AsideMainButton
                        icon={<LibraryBig />}
                        label="Minhas matérias"
                        isCollapsed={false}
                        isSelected={selectedSection === 'materias'}
                    />
                </a>
                <a href="/professor/upload">
                    <AsideMainButton
                        icon={<Plus />}
                        label="Adicionar fontes"
                        isCollapsed={false}
                        isSelected={selectedSection === 'addFontes'}
                    />
                </a>
            </div>
        </div>
    );
}
