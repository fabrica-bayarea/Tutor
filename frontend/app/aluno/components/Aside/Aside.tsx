'use client';

import { useEffect, useState } from 'react';
import { usePathname, useParams } from 'next/navigation';
import styles from './Aside.module.css';
import { Menu, SquarePen } from 'lucide-react';
import AsideMainButton from '../../../components/AsideMainButton/AsideMainButton';
import ChatListItemButton from '../ChatListItemButton/ChatListItemButton';
import { InterfaceChat } from '@/app/types';

export default function Aside({ chats }: { chats: InterfaceChat[] }) {
    const pathname = usePathname();
    const params = useParams();
    
    const getSelected = () => {
        if (pathname.endsWith('/aluno')) return 'home';
        return null;
    };
    const selectedSection = getSelected();
    
    const selectedChatId = params.chatId;
    
    return (
        <div className={styles.asideContainer}>
            <div className={styles.asideHeader}>
                {/* <img src="" alt="" /> */}
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
