import StatusBadge, { StatusBadgeVariant } from '../StatusBadge/StatusBadge';
import Button from '../Button/Button';
import styles from './QuestionCard.module.css';

type QuestionCardProps = {
    question: string;
    status: StatusBadgeVariant;
    context?: string;
    onRespond?: () => void;
    onViewContext?: () => void;
    className?: string;
};

export default function QuestionCard({
    question,
    status,
    context,
    onRespond,
    onViewContext,
    className,
}: QuestionCardProps) {
    return (
        <div className={[styles.card, className ?? ''].filter(Boolean).join(' ')}>
            <div className={styles.header}>
                <p className={styles.question}>{question}</p>
                <StatusBadge variant={status} />
            </div>

            {context && <p className={styles.context}>{context}</p>}

            {(onViewContext || onRespond) && (
                <div className={styles.footer}>
                    {onViewContext && (
                        <Button
                            style="ghost"
                            size="sm"
                            label="Contexto da conversa"
                            onClick={onViewContext}
                        />
                    )}
                    {onRespond && (
                        <Button
                            style="filled"
                            action="primary"
                            size="sm"
                            label="Responder"
                            onClick={onRespond}
                        />
                    )}
                </div>
            )}
        </div>
    );
}
