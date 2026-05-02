import { SendHorizonal } from "lucide-react"
import styles from "./TextArea.module.css"
import { useState } from "react";

interface TextAreaProps {
  isDisabled: boolean;
  value: string;
  onChange: (val: string) => void;
  onSend: (text: string) => void;
}

export default function TextArea({isDisabled, value, onChange, onSend}: TextAreaProps){

    const handleSendClick = () => {
    if (!value.trim()) return;
    onSend(value);
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault(); 
        handleSendClick();
    }
    };

    return(
        <section className={styles.textAreaSection}>
            <textarea 
            disabled={isDisabled}
            placeholder="Envie aqui sua dúvida"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            />
            <button onClick={handleSendClick}><SendHorizonal color="white" size={14}/></button>
        </section>
    )
}