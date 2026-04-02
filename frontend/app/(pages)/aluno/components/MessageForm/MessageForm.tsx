import { useRef, useState } from 'react';
import { SendHorizonal, Paperclip } from 'lucide-react';
import styles from './MessageForm.module.css';
import Select from 'react-select';

import IconButton from '../../../../components/IconButton/IconButton';



interface MessageFormProps {
    onSendMessage: (message: string) => void;
    isDisabled?: boolean;
}

export default function MessageForm({ onSendMessage, isDisabled }: MessageFormProps) {
    const [messageText, setMessageText] = useState('');
    const formRef = useRef<HTMLFormElement>(null)


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

    function handleMessageKeyDown(event: React.KeyboardEvent<HTMLTextAreaElement>) {
       // console.log('funciona')
        if(event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            formRef.current?.requestSubmit()
        } 
    }

    const isMessageTextEmpty = messageText.length === 0;

    return (
        <form ref={formRef} className={styles.messageFormContainer} onSubmit={handleSendMessage}>
            <textarea
                name="message"
                placeholder="Digite uma mensagem"
                value={messageText}
                onChange={handleMessageTextChange}
                onKeyDown={handleMessageKeyDown}
                disabled={isDisabled}
            />
            <div className={styles.chatControls}>
                <Select
                    className={styles.materiaPadding}
                    placeholder="Matéria"
                    required
                    //options={options}
                    //onChange={handleVinculosChange}
                />
                 <Select
                    placeholder="IA"
                    required
                    //options={options}
                    //onChange={handleVinculosChange}
                />
                <div className={styles.messageFormButtonContainer}>
                    <button type="submit" disabled={isMessageTextEmpty || isDisabled} title="Enviar mensagem">
                        <SendHorizonal size={24} />
                    </button>
                </div>
            </div>
        </form>
    );
}
