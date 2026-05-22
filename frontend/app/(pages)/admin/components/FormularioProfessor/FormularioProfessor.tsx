"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { criarProfessor, atualizarProfessor } from "../../../../services/service_professor";
import { useToast } from "@/contexts/ToastContext";
import styles from "./formulario.professor.module.css";

interface FormularioProfessorProps {
    mode: "novoProfessor" | "editarProfessor";
    initialId?: string;
    initialNome?: string;
    initialMatricula?: string;
    initialEmail?: string;
}

type CampoErros = {
    nome?: string;
    matricula?: string;
    email?: string;
    geral?: string;
};

function emailInstitucionalValido(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) && email.endsWith("@iesb.edu.br");
}

export default function FormularioProfessor({
    mode,
    initialId = "",
    initialNome = "",
    initialMatricula = "",
    initialEmail = "",
}: FormularioProfessorProps) {
    const router = useRouter();
    const { addToast } = useToast();
    const isEdit = mode === "editarProfessor";
    const textoBotao = isEdit ? "Salvar" : "Cadastrar";

    const [nome, setNome] = useState(initialNome);
    const [matricula, setMatricula] = useState(initialMatricula);
    const [email, setEmail] = useState(initialEmail);
    const [erros, setErros] = useState<CampoErros>({});
    const [submitting, setSubmitting] = useState(false);

    function validarLocal(): CampoErros {
        const e: CampoErros = {};
        if (!nome.trim()) e.nome = "Informe o nome completo.";
        if (!matricula.trim()) e.matricula = "Informe a matrícula.";
        if (!email.trim()) e.email = "Informe o e-mail.";
        else if (!emailInstitucionalValido(email.trim()))
            e.email = "Informe um e-mail institucional válido (@iesb.edu.br).";
        return e;
    }

    function handleCancelar() {
        router.push("/admin/pages/professores");
    }

    function tratarErroDuplicado(message: string): CampoErros {
        const msg = message.toLowerCase();
        const next: CampoErros = {};
        if (msg.includes("matrícula") || msg.includes("matricula")) {
            next.matricula = "Matrícula já cadastrada.";
        }
        if (msg.includes("email") || msg.includes("e-mail")) {
            next.email = "E-mail já cadastrado.";
        }
        if (!next.matricula && !next.email) {
            next.matricula = "Matrícula já cadastrada.";
            next.email = "E-mail já cadastrado.";
        }
        return next;
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
            const resultado = await atualizarProfessor(
                initialId,
                initialMatricula,
                nome.trim(),
                email.trim()
            );
            setSubmitting(false);
            if (resultado.ok) {
                addToast("Professor atualizado com sucesso.", "success");
                router.push("/admin/pages/professores");
                return;
            }
            if (resultado.status === 409) {
                setErros(tratarErroDuplicado(resultado.message));
                return;
            }
            setErros({ geral: resultado.message });
            return;
        }

        const resultado = await criarProfessor(
            matricula.trim(),
            nome.trim(),
            email.trim()
        );
        setSubmitting(false);

        if (resultado.ok) {
            addToast("Professor cadastrado! Um link de convite foi enviado para o e-mail informado.", "success");
            router.push("/admin/pages/professores");
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
                        <span>Nome completo</span>
                        <input
                            type="text"
                            id="nomeProfessor"
                            value={nome}
                            onChange={(e) => setNome(e.target.value)}
                            aria-invalid={!!erros.nome}
                        />
                        {erros.nome && <p className={styles.errorMsg}>{erros.nome}</p>}
                    </div>

                    <div className={styles.field}>
                        <span>Matrícula institucional</span>
                        <input
                            className={styles.matricula}
                            disabled={isEdit}
                            type="text"
                            id="matriculaProfessor"
                            value={matricula}
                            onChange={(e) => setMatricula(e.target.value)}
                            aria-invalid={!!erros.matricula}
                        />
                        {erros.matricula && (
                            <p className={styles.errorMsg}>{erros.matricula}</p>
                        )}
                    </div>

                    <div className={styles.field}>
                        <span>E-mail institucional</span>
                        <input
                            className={styles.email}
                            type="email"
                            id="emailProfessor"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            aria-invalid={!!erros.email}
                        />
                        {erros.email && <p className={styles.errorMsg}>{erros.email}</p>}
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
