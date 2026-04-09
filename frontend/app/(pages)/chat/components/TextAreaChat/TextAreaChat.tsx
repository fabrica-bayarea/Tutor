import { Plus, SendHorizontal } from "lucide-react";
import styles from "./TextAreaChat.module.css";

interface TextAreaChatProps {
  isDisabled : boolean;
  value: string;
  onChange: (val: string) => void;
  onSend: () => void;
  onPlusClick?: () => void;
}

export default function TextAreaChat({
  isDisabled,
  value,
  onChange,
  onSend,
  onPlusClick,
}: TextAreaChatProps) {
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
          />
          <SendHorizontal size={24} onClick={onSend} />
        </article>
      </section>

      <section className={styles.textareaDeskTop}>
        <textarea
          placeholder="Envie aqui sua dúvida"
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
        <article>
          <Plus size={24} onClick={onPlusClick} />
          <SendHorizontal size={24} onClick={onSend} />
        </article>
      </section>
    </section>
  );
}
