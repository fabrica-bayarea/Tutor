"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { criarMateria, atualizarMateria } from "../../../../services/service_materia";
import { useToast } from "@/contexts/ToastContext";
import styles from "./formulario.materia.module.css";

interface FormularioMateriaProps {
    mode: "novaMateria" | "editarMateria";
    initialId?: string;
    initialCodigo?: string;
    initialNome?: string;
    initialStatus?: string;
}

type CampoErros = {
    codigo?: string;
    nome?: string;
    geral?: string;
};

export default function FormularioMateria({
    mode,
    initialId = "",
    initialCodigo = "",
    initialNome = "",
    initialStatus = "ATIVO",
}: FormularioMateriaProps) {
    const router = useRouter();
    const { addToast } = useToast();
    const isEdit = mode === "editarMateria";
    const textoBotao = isEdit ? "Salvar" : "Cadastrar";

    const [codigo, setCodigo] = useState(initialCodigo);
    const [nome, setNome] = useState(initialNome);
    const [erros, setErros] = useState<CampoErros>({});
    const [submitting, setSubmitting] = useState(false);

    function validarLocal(): CampoErros {
        const e: CampoErros = {};
        if (!codigo.trim()) e.codigo = "Informe o código.";
        if (!nome.trim()) e.nome = "Informe o nome.";
        return e;
    }

    function handleCancelar() {
        router.push("/admin/pages/materias");
    }

    function tratarErroDuplicado(message: string): CampoErros {
        const msg = message.toLowerCase();
        if (msg.includes("código") || msg.includes("codigo")) {
            return { codigo: "Já existe uma matéria com este código." };
        }
        return { codigo: "Já existe uma matéria com este código." };
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

        if (isEdit) {
            const resultado = await atualizarMateria(
                initialId,
                codigo.trim(),
                nome.trim(),
                initialStatus
            );
            setSubmitting(false);
            if (resultado.ok) {
                addToast("Matéria atualizada com sucesso.", "success");
                router.push("/admin/pages/materias");
                return;
            }
            if (resultado.status === 409) {
                setErros(tratarErroDuplicado(resultado.message));
                return;
            }
            setErros({ geral: resultado.message });
            return;
        }

        const resultado = await criarMateria(codigo.trim(), nome.trim());
        setSubmitting(false);

        if (resultado.ok) {
            addToast("Matéria cadastrada com sucesso.", "success");
            router.push("/admin/pages/materias");
            return;
        }

        if (resultado.status === 409) {
            setErros(tratarErroDuplicado(resultado.message));
            return;
        }

        setErros({ geral: resultado.message });
    }

    return (
        <form onSubmit={handleSubmit} noValidate>
            <div>
                <div className={styles.cadastro}>
                    <div className={styles.field}>
                        <span>Nome da matéria</span>
                        <input
                            type="text"
                            id="nomeMateria"
                            value={nome}
                            onChange={(e) => setNome(e.target.value)}
                            aria-invalid={!!erros.nome}
                            maxLength={64}
                        />
                        {erros.nome && <p className={styles.errorMsg}>{erros.nome}</p>}
                    </div>

                    <div className={styles.field}>
                        <span> {isEdit ? "Código da matéria (não editável)" : "Código da matéria"}</span>
                        <input
                            type="text"
                            id="codigoMateria"
                            disabled={isEdit}
                            value={codigo}
                            onChange={(e) => setCodigo(e.target.value)}
                            aria-invalid={!!erros.codigo}
                            maxLength={10}
                        />
                        {erros.codigo && <p className={styles.errorMsg}>{erros.codigo}</p>}
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
