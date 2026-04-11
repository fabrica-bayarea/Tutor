import { Plus, SendHorizontal } from "lucide-react";
import styles from "./TextAreaChat.module.css";

interface TextAreaChatProps {
  isDisabled: boolean;
  value: string;
  onChange: (val: string) => void;
  onSend: (text: string) => void;
  onPlusClick?: () => void;
}

export default function TextAreaChat({
  isDisabled,
  value,
  onChange,
  onSend,
  onPlusClick,
}: TextAreaChatProps) {

  const handleSendClick = () => {
    if (!value.trim()) return;
    onSend(value);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault(); // impede quebra de linha
      handleSendClick();
    }
  };

  return (
    <section className={styles.conteinerTextarea}>
      <section className={styles.textareaMobile}>
        <article className={styles.articlePlus} onClick={onPlusClick}>
          <Plus size={24} />
        </article>

        <article className={styles.articleSend}>
          <textarea
            disabled={isDisabled}
            placeholder="Envie aqui sua dúvida"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <SendHorizontal size={24} onClick={handleSendClick} />
        </article>
      </section>

      <section className={styles.textareaDeskTop}>
        <textarea
          disabled={isDisabled}
          placeholder="Envie aqui sua dúvida"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        <article>
          <Plus size={24} onClick={onPlusClick} />
          <SendHorizontal size={24} onClick={handleSendClick} />
        </article>
      </section>
    </section>
  );
}