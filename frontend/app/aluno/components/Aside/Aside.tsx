import { useState } from 'react';
import styles from './Aside.module.css';
import { Menu, SquarePen } from 'lucide-react';
import AsideMainButton from '../../../components/AsideMainButton/AsideMainButton';
import ChatListItemButton from '../ChatListItemButton/ChatListItemButton';
type AsideAlunoProps = {
    selected: 'home';
};

export default function Aside({ selected }: AsideAlunoProps) {
    const [chats, setChats] = useState([
        {
            id: 'af734cdf-1106-49ec-8b26-be87598c992c',
            aluno_id: 'cde982bc-2c4b-43a0-8439-eba9d2149306',
            name: 'Chat de teste',
        },
    ]);
    return (
        <div className={styles.asideContainer}>
            <div className={styles.asideHeader}>
                <img src="" alt="" />
                <Menu size={24} />
            </div>
            <div className={styles.asideMainButtons}>
                <AsideMainButton
                    icon={<SquarePen />}
                    label="Novo chat"
                    isCollapsed={false}
                    isSelected={selected === 'home'}
                />
            </div>
            <div className={styles.asideChatList}>
                {chats.map((chat) => (
                    <ChatListItemButton
                        key={chat.id}
                        id={chat.id}
                        aluno_id={chat.aluno_id}
                        name={chat.name}
                        isSelected={chat.id === selected}
                    />
                ))}
            </div>
        </div>
    );
}
