'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import styles from './Aside.module.css';
import { House, Book, GraduationCap, FolderPlus, ChartColumn, MessageCircleMore, Bolt, Ban, ChevronRight, Folder } from 'lucide-react';
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
        <>
            <div className={styles.asideContainer}>
                <div className={styles.tituloNav}><h1>DashBoard</h1></div>
            <div className={styles.asideHeader}>
                <img src="null" alt="" />
            </div>
            <div className={styles.asideMainButtons}>

                <div className={styles.asideCriarChatButton}>
                    <a href="/professor">
                    <button className={styles.newChatButton}>
                        <House/>
                        Visão Geral
                        <ChevronRight/>
                    </button>
                    </a>
                </div>

                <div className={styles.asideCriarChatButton}>
                    <a href="/professor/materias">
                    <button className={styles.newChatButton}>
                        <Book/>
                        Minhas Matérias
                        <ChevronRight/>
                    </button>
                    </a>
                </div>

                <div className={styles.asideCriarChatButton}>
                    <a href="/professor/turmas">
                    <button className={styles.newChatButton}>
                        <GraduationCap/>
                        Minhas Turmas
                        <ChevronRight/>
                    </button>
                    </a>
                </div>

                <div className={styles.asideCriarChatButton}>
                    <a href="/professor/upload">
                    <button className={styles.newChatButton}>
                        <FolderPlus/>
                        Adicionar Fontes
                        <ChevronRight/>
                    </button>
                    </a>
                </div>

                <div className={styles.asideCriarChatButton}>
                    <a href="/professor/estatisticas">
                    <button className={styles.newChatButton}>
                        <ChartColumn/>
                        Estatísticas
                        <ChevronRight/>
                    </button>
                    </a>
                </div>

                <div className={styles.asideCriarChatButton}>
                    <a href="/professor/chat">
                    <button className={styles.newChatButton}>
                        <MessageCircleMore/>
                        Chat
                        <ChevronRight/>
                    </button>
                    </a>
                </div>  

                <div className={styles.divAsideOtrButtons}>
                    <div className={styles.asideOtrButton}>
                        <a href="/configuracao">
                        <button className={styles.otrButton}>
                            <Bolt/>
                            Configuração
                        </button>
                        </a>
                    </div>

                    <div className={styles.asideOtrButton}>
                        <a href="/sair">
                        <button className={styles.otrButton}>
                            <Ban/>
                            Sair
                        </button>
                        </a>
                    </div>
                </div>

            </div>
        </div>
        </>
    );
}
