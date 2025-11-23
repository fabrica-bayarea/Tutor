'use client';

import { usePathname, useParams } from 'next/navigation';
import styles from './AsideChat.module.css';
import { MessageCircleMore, Bolt, Ban, Coffee } from 'lucide-react';
import ChatListItemButton from '../../../aluno/components/ChatListItemButton/ChatListItemButton';
import { InterfaceChat } from '@/app/types';

export default function AsideChat({ chats }: { chats: InterfaceChat[] }) {
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
            <div className={styles.asideContainerProf}>
                <div className={styles.tituloNavProf}><h1>Tutor AI</h1></div>

                <div className={styles.asideCriarChatButtonProf}>
                    <a href="/aluno">
                    <button className={styles.newChatButtonProf}>
                        <MessageCircleMore/>
                        Novo Chat
                    </button>
                    </a>
                </div>

                <div>
                    <p>Chats</p>
                    <div className={styles.asideChatListProf}>
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
                
                <div className={styles.divAsideOtrButtonsProf}>
                    <div className={styles.asideOtrButtonProf}>
                        <a href="/configuracao">
                        <button className={styles.otrButtonProf}>
                            <Bolt/>
                            Configuração
                        </button>
                        </a>
                    </div>

                    <div className={styles.asideOtrButtonProf}>
                        <div>
                        <a href="/professor">
                        <button className={styles.otrButtonProf}>
                            <Coffee/>
                            Área do Professor
                        </button>
                        </a>
                        </div>
                    </div>

                    <div className={styles.asideOtrButtonProf}>
                        <div>
                        <a href="/sair">
                        <button className={styles.otrButtonProf}>
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
