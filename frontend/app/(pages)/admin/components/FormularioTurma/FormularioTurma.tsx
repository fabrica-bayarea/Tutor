"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { criarTurma, atualizarTurma } from "../../../../services/service_turma";
import { useToast } from "@/contexts/ToastContext";
import Select, { SelectOption } from "../../../../components/Select/Select";
import {
    TURNO_DISPLAY_OPTIONS,
    turnoApiToDisplay,
    turnoDisplayToApi,
    SEMESTRE_REGEX,
} from "@/utils/turno";
import styles from "./formulario.turma.module.css";

interface FormularioTurmaProps {
    mode: "novaTurma" | "editarTurma";
    initialId?: string;
    initialCodigo?: string;
    initialSemestre?: string;
    initialTurno?: string;
    initialStatus?: string;
}

type CampoErros = {
    codigo?: string;
    semestre?: string;
    turno?: string;
    geral?: string;
};

const TURNO_OPTIONS: SelectOption[] = TURNO_DISPLAY_OPTIONS.map((t) => ({
    value: t,
    label: t,
}));

export default function FormularioTurma({
    mode,
    initialId = "",
    initialCodigo = "",
    initialSemestre = "",
    initialTurno = "",
    initialStatus = "ATIVO",
}: FormularioTurmaProps) {
    const router = useRouter();
    const { addToast } = useToast();
    const isEdit = mode === "editarTurma";
    const textoBotao = isEdit ? "Salvar" : "Cadastrar";

    const [codigo, setCodigo] = useState(initialCodigo);
    const [semestre, setSemestre] = useState(initialSemestre);
    const [turnoDisplay, setTurnoDisplay] = useState(
        initialTurno ? turnoApiToDisplay(initialTurno) : ""
    );
    const [erros, setErros] = useState<CampoErros>({});
    const [submitting, setSubmitting] = useState(false);

    function validarLocal(): CampoErros {
        const e: CampoErros = {};
        if (!codigo.trim()) e.codigo = "Informe o código.";
        if (!semestre.trim()) e.semestre = "Informe o semestre.";
        else if (!SEMESTRE_REGEX.test(semestre.trim()))
            e.semestre = "Formato inválido. Use o padrão AAAA.S (ex: 2026.1).";
        if (!turnoDisplay) e.turno = "Selecione o turno.";
        return e;
    }

    function handleCancelar() {
        router.push("/admin/pages/turmas");
    }

    function tratarErroDuplicado(): CampoErros {
        return { codigo: "Já existe uma turma com este código." };
    }

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        if (submitting) return;

        const errosLocais = validarLocal();
        if (Object.keys(errosLocais).length > 0) {
            setErros(errosLocais);
            return;
        }

        setErros({});
        setSubmitting(true);

        const turnoApi = turnoDisplayToApi(turnoDisplay);

        if (isEdit) {
            const resultado = await atualizarTurma(
                initialId,
                codigo.trim(),
                semestre.trim(),
                turnoApi,
                initialStatus
            );
            setSubmitting(false);
            if (resultado.ok) {
                addToast("Turma atualizada com sucesso.", "success");
                router.push("/admin/pages/turmas");
                return;
            }
            if (resultado.status === 409) {
                setErros(tratarErroDuplicado());
                return;
            }
            setErros({ geral: resultado.message });
            return;
        }

        const resultado = await criarTurma(
            codigo.trim(),
            semestre.trim(),
            turnoApi
        );
        setSubmitting(false);

        if (resultado.ok) {
            addToast("Turma cadastrada com sucesso.", "success");
            router.push("/admin/pages/turmas");
            return;
        }

        if (resultado.status === 409) {
            setErros(tratarErroDuplicado());
            return;
        }

        setErros({ geral: resultado.message });
    }

    const turnoSelecionado =
        TURNO_OPTIONS.find((opt) => opt.value === turnoDisplay) ?? null;

    return (
        <form onSubmit={handleSubmit} noValidate>
            <div>
                <div className={styles.cadastro}>
                    <div className={styles.field}>
                        <span>
                            {isEdit ? "Código da turma (não editável)" : "Código da turma"}
                        </span>
                        <input
                            type="text"
                            id="codigoTurma"
                            disabled={isEdit}
                            value={codigo}
                            onChange={(e) => setCodigo(e.target.value)}
                            aria-invalid={!!erros.codigo}
                            maxLength={8}
                        />
                        {erros.codigo && (
                            <p className={styles.errorMsg}>{erros.codigo}</p>
                        )}
                    </div>

                    <div className={styles.field}>
                        <span>Semestre</span>
                        <input
                            type="text"
                            id="semestreTurma"
                            value={semestre}
                            onChange={(e) => setSemestre(e.target.value)}
                            aria-invalid={!!erros.semestre}
                            maxLength={6}
                            placeholder="Ex: 2026.1"
                        />
                        {erros.semestre && (
                            <p className={styles.errorMsg}>{erros.semestre}</p>
                        )}
                    </div>

                    <div className={styles.field}>
                        <span>Turno</span>
                        <Select
                            instanceId="turnoTurma"
                            options={TURNO_OPTIONS}
                            value={turnoSelecionado}
                            onChange={(opt) => {
                                const selected = opt as SelectOption | null;
                                setTurnoDisplay(selected?.value ?? "");
                            }}
                            placeholder="Selecione o turno"
                            isSearchable={false}
                        />
                        {erros.turno && (
                            <p className={styles.errorMsg}>{erros.turno}</p>
                        )}
                    </div>

                    {erros.geral && <p className={styles.errorGeral}>{erros.geral}</p>}

                    <div className={styles.buttonContainer}>
                        <button
                            type="button"
                            className={styles.botaoCancelar}
                            onClick={handleCancelar}
                            disabled={submitting}
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            className={styles.botaoSalvar}
                            disabled={submitting}
                        >
                            {submitting ? "Salvando..." : textoBotao}
                        </button>
                    </div>
                </div>
            </div>
        </form>
    );
}
