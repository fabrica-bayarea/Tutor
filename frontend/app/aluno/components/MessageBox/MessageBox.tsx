import styles from './MessageBox.module.css';
import { LLM_UUID } from '@/constants';

import { InterfaceMensagem } from '../../../types';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function MessageBox({
    id,
    chat_id,
    sender_id,
    conteudo,
    data_envio,
}: InterfaceMensagem) {
    const isUser = sender_id !== LLM_UUID;

    return (
        <div className={`${styles.messageBoxContainer} ${isUser ? styles.fromUser : ''}` }>
            <div className={`${styles.messageBox} ${isUser ? styles.fromUser : styles.fromSystem}`}>
                <h4 className={styles.messageAuthor}>{isUser ? 'Você' : 'Tutor 24h'}</h4>
                <div className={styles.messageContent}>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{conteudo}</ReactMarkdown>
                </div>
            </div>
        </div>
    );
}
