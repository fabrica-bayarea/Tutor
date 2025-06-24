'use client';

import { useEffect, useState } from 'react';
import { usePathname, useParams } from 'next/navigation';
import styles from './Aside.module.css';
import { Menu, SquarePen } from 'lucide-react';
import AsideMainButton from '../../../components/AsideMainButton/AsideMainButton';
import ChatListItemButton from '../ChatListItemButton/ChatListItemButton';
import { InterfaceChat } from '../../../types';

export default function Aside() {
    const pathname = usePathname();
    const params = useParams();
    
    const getSelected = () => {
        if (pathname.endsWith('/aluno')) return 'home';
        return null;
    };
    const selectedSection = getSelected();
    
    const [chats, setChats] = useState<InterfaceChat[]>([
        {
            id: 'af734cdf-1106-49ec-8b26-be87598c992c',
            aluno_id: 'cde982bc-2c4b-43a0-8439-eba9d2149306',
            nome: 'Chat de teste',
        },
    ]);
    
    const selectedChatId = params.chatId;
    useEffect(() => {
        
    }, []);
    
    return (
        <div className={styles.asideContainer}>
            <div className={styles.asideHeader}>
                <img src="" alt="" />
                <Menu size={24} />
            </div>
            <div className={styles.asideMainButtons}>
                <a href="/aluno">
                    <AsideMainButton
                        icon={<SquarePen />}
                        label="Novo chat"
                        isCollapsed={false}
                        isSelected={selectedSection === 'home'}
                    />
                </a>
            </div>
            <div className={styles.asideChatList}>
                {chats.map((chat) => (
                    <ChatListItemButton
                        key={chat.id}
                        id={chat.id}
                        aluno_id={chat.aluno_id}
                        name={chat.nome}
                        isSelected={chat.id === selectedChatId}
                    />
                ))}
            </div>
        </div>
    );
}
