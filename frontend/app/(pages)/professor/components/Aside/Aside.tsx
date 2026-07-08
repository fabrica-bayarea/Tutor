'use client';

import { usePathname, useRouter } from 'next/navigation';
import { House, Book, GraduationCap, FolderPlus, ChartColumn, MessageCircleMore, BookOpen, Settings, LogOut } from 'lucide-react';
import AsideMainButton from '../../../../components/AsideMainButton/AsideMainButton';
import Button from '../../../../components/Button/Button';
import { logout } from '@/app/services/service_auth';
import styles from './Aside.module.css';

export default function Aside() {
    const pathname = usePathname();
    const router = useRouter();

    const handleSair = async () => {
        await logout();
        // Redireciona após remover o cookie de sessão (US-05-RN1/RI1).
        window.location.replace('/tutor/login');
    };

    const getSelected = () => {
        if (pathname?.endsWith('/professor')) return 'home';
        if (pathname?.includes('/professor/pages/turmas')) return 'turmas';
        if (pathname?.includes('/professor/pages/materias')) return 'materias';
        if (pathname?.includes('/professor/pages/upload')) return 'addFontes';
        if (pathname?.includes('/professor/pages/estatisticas')) return 'estatisticas';
        return null;
    };

    const selected = getSelected();

    return (
        <div className={styles.asideContainer}>
            <div>
                <div className={styles.sectionTitle}>
                    <BookOpen size={20} color="#0d9488" />
                    <h1>Tutor</h1>
                </div>
                <div className={styles.asideMainButtons}>
                    <AsideMainButton
                        icon={<House size={16} />}
                        label="Visão Geral"
                        isSelected={selected === 'home'}
                        onClick={() => router.push('/professor')}
                    />
                    <AsideMainButton
                        icon={<Book size={16} />}
                        label="Minhas Matérias"
                        isSelected={selected === 'materias'}
                        onClick={() => router.push('/professor/pages/materias')}
                    />
                    <AsideMainButton
                        icon={<GraduationCap size={16} />}
                        label="Minhas Turmas"
                        isSelected={selected === 'turmas'}
                        onClick={() => router.push('/professor/pages/turmas')}
                    />
                    <AsideMainButton
                        icon={<FolderPlus size={16} />}
                        label="Adicionar Fontes"
                        isSelected={selected === 'addFontes'}
                        onClick={() => router.push('/professor/pages/upload')}
                    />
                    <AsideMainButton
                        icon={<ChartColumn size={16} />}
                        label="Estatísticas"
                        isSelected={selected === 'estatisticas'}
                        onClick={() => router.push('/professor/pages/estatisticas')}
                    />
                    <AsideMainButton
                        icon={<MessageCircleMore size={16} />}
                        label="Chat"
                        onClick={() => router.push('/chat')}
                    />
                </div>
            </div>

            <div className={styles.asideFooter}>
                <Button
                    style="ghost"
                    icon={<Settings size={16} />}
                    label="Configurações"
                    fullWidth
                />
                <Button
                    style="ghost"
                    icon={<LogOut size={16} />}
                    label="Sair"
                    fullWidth
                    onClick={handleSair}
                />
            </div>
        </div>
    );
}
