import styles from './StatusBadge.module.css';

export type StatusBadgeVariant =
    | 'ativa'
    | 'respondida'
    | 'desativada'
    | 'erro'
    | 'processando'
    | 'pendente'
    | 'aguardando'
    | 'disponivel'
    | 'na-fila'
    | 'inativa';

type StatusBadgeProps = {
    variant: StatusBadgeVariant;
    label?: string;
    className?: string;
};

const defaultLabels: Record<StatusBadgeVariant, string> = {
    ativa: 'Ativa',
    respondida: 'Respondida',
    desativada: 'Desativada',
    erro: 'Erro',
    processando: 'Processando',
    pendente: 'Pendente',
    aguardando: 'Aguardando',
    disponivel: 'Disponível',
    'na-fila': 'Na fila',
    inativa: 'Inativa',
};

export default function StatusBadge({ variant, label, className }: StatusBadgeProps) {
    return (
        <span
            className={[styles.badge, styles[variant as keyof typeof styles], className ?? ''].filter(Boolean).join(' ')}
        >
            {label ?? defaultLabels[variant]}
        </span>
    );
}
