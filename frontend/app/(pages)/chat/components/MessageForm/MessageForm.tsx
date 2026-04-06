import { useState } from 'react';
import { SendHorizonal, Paperclip } from 'lucide-react';
import styles from './MessageForm.module.css';

import IconButton from '../../../../components/IconButton/IconButton';

interface MessageFormProps {
    onSendMessage: (message: string) => void;
    isDisabled?: boolean;
}

export default function MessageForm({ onSendMessage, isDisabled }: MessageFormProps) {
    const [messageText, setMessageText] = useState('');
    console.log(messageText); // teste

    function handleMessageTextChange(event: React.ChangeEvent<HTMLTextAreaElement>) {
        event.target.setCustomValidity('');
        setMessageText(event.target.value);
    }

    function handleSendMessage(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();
        if (!messageText.trim()) return;

        onSendMessage(messageText);
        setMessageText('');
    }

    const isMessageTextEmpty = messageText.length === 0;

    return (
        <form className={styles.messageFormContainer} onSubmit={handleSendMessage}>
            <textarea
                name="message"
                placeholder="Digite uma mensagem"
                value={messageText}
                onChange={handleMessageTextChange}
                disabled={isDisabled}
            />
            <div className={styles.messageFormButtonContainer}>
                <button type="submit" disabled={isMessageTextEmpty || isDisabled} title="Enviar mensagem">
                    <SendHorizonal size={24} />
                </button>
            </div>
        </form>
    );
}
