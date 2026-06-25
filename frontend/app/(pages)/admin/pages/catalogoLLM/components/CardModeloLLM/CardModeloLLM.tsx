"use client";

import { Bot, AlertTriangle } from "lucide-react";
import StatusBadge from "@/app/components/StatusBadge/StatusBadge";
import Button from "@/app/components/Button/Button";
import ProgressBar from "@/app/components/ProgressBar/ProgressBar";
import { InterfaceLLM } from "@/app/types";
import { usePullProgress } from "../../hooks/usePullProgress";
import styles from "./CardModeloLLM.module.css";

type CardModeloLLMProps = {
    modelo: InterfaceLLM;
    onAtivar: (modelo: InterfaceLLM) => void;
};

export default function CardModeloLLM({ modelo, onAtivar }: CardModeloLLMProps) {
    const ehAtivo = modelo.status === "ativada";

    // Modelo ativo já está instalado: não há por que consultar o pull-status.
    // Para os demais, o hook faz uma leitura no mount e mantém o polling apenas
    // enquanto o download estiver em andamento.
    const { progresso, fase } = usePullProgress(modelo.id, { enabled: !ehAtivo });

    const percent = progresso?.percent ?? 0;

    return (
        <div className={`${styles.card} ${ehAtivo ? styles.cardAtivo : ""}`}>
            <div className={styles.topo}>
                <div className={styles.info}>
                    <span className={styles.iconeWrap}>
                        <Bot size={20} />
                    </span>
                    <h3 className={styles.nome} title={modelo.nome}>
                        {modelo.nome}
                    </h3>
                </div>

                <div className={styles.acao}>
                    {ehAtivo && <StatusBadge variant="ativa" label="Ativo" />}

                    {!ehAtivo && fase === "concluido" && (
                        <Button
                            style="filled"
                            action="primary"
                            size="sm"
                            label="Ativar"
                            onClick={() => onAtivar(modelo)}
                        />
                    )}

                    {!ehAtivo && fase === "baixando" && (
                        <StatusBadge variant="processando" label="Baixando" />
                    )}

                    {!ehAtivo && fase === "erro" && <StatusBadge variant="erro" label="Erro" />}

                    {!ehAtivo && fase === null && (
                        <span className={styles.verificando}>Verificando...</span>
                    )}
                </div>
            </div>

            {!ehAtivo && fase === "baixando" && (
                <div className={styles.progressoArea}>
                    <ProgressBar value={percent} />
                    <div className={styles.progressoTopo}>
                        <span>Baixando modelo...</span>
                        <span className={styles.percent}>{percent}%</span>
                    </div>
                </div>
            )}

            {!ehAtivo && fase === "erro" && (
                <div className={styles.progressoArea}>
                    <ProgressBar value={percent} color="#dc2626" />
                    <div className={styles.erro}>
                        <AlertTriangle size={16} />
                        <span>Falha ao baixar o modelo. Verifique a conexão e tente novamente.</span>
                    </div>
                </div>
            )}
        </div>
    );
}
