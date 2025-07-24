import styles from './ChatListItemButton.module.css';
import IconButton from '../../../../components/IconButton/IconButton';
import { Ellipsis } from 'lucide-react';

interface ChatListItemButtonProps {
    id: string;
    aluno_id: string;
    name: string;
    isSelected?: boolean;
}

export default function ChatListItemButton({
    id,
    aluno_id,
    name,
    isSelected,
}: ChatListItemButtonProps) {
    return (
        <div className={styles.chatListItemButton}>
            <div className={`${styles.chatListItemButtonStateLayer} ${isSelected ? styles.selected : ''}`}>
                <a title={name} href={`/aluno/chat/${id}`} className={styles.chatListItemButtonName}>
                    {name}
                </a>
                <IconButton icon={<Ellipsis />} />
            </div>
        </div>
    );
}
