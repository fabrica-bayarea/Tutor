'use client';

import { useEffect, useState } from 'react';
import { usePathname, useParams } from 'next/navigation';
import styles from './Aside.module.css';
import { MessageCircleMore} from 'lucide-react';
import AsideMainButton from '../../../../components/AsideMainButton/AsideMainButton';
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
        <>
            <div className={styles.asideContainer}>
                <div className={styles.tituloNav}><h1>Tutor AI</h1></div>

                <div className={styles.asideCriarChatButton}>
                    <a href="/aluno">
                    <button className={styles.newChatButton}>
                        <MessageCircleMore/>
                        Novo Chat
                    </button>
                    </a>
                </div>

                <div>
                    <p>Chats</p>
                    <div className={styles.asideChatList}>
                        {chats
                            .slice()
                            .reverse()
                            .map((chat) => (
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

            </div>
        </>
    );
}
