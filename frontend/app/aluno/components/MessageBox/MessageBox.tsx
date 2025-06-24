import styles from './MessageBox.module.css';

import { InterfaceMensagem } from '../../../types';

export default function MessageBox({
    id,
    chat_id,
    sender_id,
    conteudo,
    data_envio,
}: InterfaceMensagem) {
    const isUser = sender_id === 'cde982bc-2c4b-43a0-8439-eba9d2149306';

    return (
        <div className={`${styles.messageBoxContainer} ${isUser ? styles.fromUser : ''}` }>
            <div className={`${styles.messageBox} ${isUser ? styles.fromUser : styles.fromSystem}`}>
                <h4 className={styles.messageAuthor}>{isUser ? 'Você' : 'Tutor 24h'}</h4>
                <p className={styles.messageContent}>{conteudo}</p>
            </div>
        </div>
    );
}
