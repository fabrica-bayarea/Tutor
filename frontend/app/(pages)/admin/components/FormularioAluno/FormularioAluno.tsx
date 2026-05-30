"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { criarAluno, atualizarAluno } from "../../../../services/service_aluno";
import { useToast } from "@/contexts/ToastContext";
import styles from "./formulario.aluno.module.css";

interface FormularioAlunoProps {
    mode: string;
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

function gerarSenhaTemporaria(): string {
    const bytes = new Uint8Array(12);
    if (typeof crypto !== "undefined" && crypto.getRandomValues) {
        crypto.getRandomValues(bytes);
    } else {
        for (let i = 0; i < bytes.length; i++) bytes[i] = Math.floor(Math.random() * 256);
    }
    return Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
}

function emailValido(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export default function FormularioAluno({
    mode,
    initialId = "",
    initialNome = "",
    initialMatricula = "",
    initialEmail = "",
}: FormularioAlunoProps) {
    const router = useRouter();
    const { addToast } = useToast();
    const isEdit = mode === "editarAluno";
    const textoBotao = isEdit ? "Salvar" : "Criar";

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
        else if (!emailValido(email)) e.email = "E-mail inválido.";
        return e;
    }

    function handleCancelar() {
        router.push("/admin/pages/alunos");
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
            const resultado = await atualizarAluno(initialId, initialMatricula, nome.trim(), email.trim());
            setSubmitting(false);
            if (resultado.ok) {
                addToast("Dados atualizados com sucesso.", "success");
                router.push("/admin/pages/alunos");
                return;
            }
            if (resultado.status === 409) {
                setErros({ email: "E-mail já cadastrado." });
                return;
            }
            setErros({ geral: resultado.message });
            return;
        }

        const resultado = await criarAluno(
            matricula.trim(),
            nome.trim(),
            email.trim(),
            gerarSenhaTemporaria()
        );

        setSubmitting(false);

        if (resultado.ok) {
            addToast("Aluno cadastrado! Um link de convite foi enviado para o e-mail informado.", "success");
            router.push("/admin/pages/alunos");
            return;
        }

        if (resultado.status === 409) {
            const msg = resultado.message.toLowerCase();
            const next: CampoErros = {};
            if (msg.includes("matrícula") || msg.includes("matricula")) {
                next.matricula = "Esta matrícula já está em uso por outro usuário.";
            }
            if (msg.includes("email") || msg.includes("e-mail")) {
                next.email = "Este e-mail já está em uso por outro usuário.";
            }
            if (!next.matricula && !next.email) {
                next.matricula = "Esta matrícula já está em uso por outro usuário.";
                next.email = "Este e-mail já está em uso por outro usuário.";
            }
            setErros(next);
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
                            id="alunoNovo"
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
                            id="matricula"
                            value={matricula}
                            onChange={(e) => setMatricula(e.target.value)}
                            aria-invalid={!!erros.matricula}
                        />
                        {erros.matricula && (
                            <p className={styles.errorMsg}>{erros.matricula}</p>
                        )}
                    </div>

                    <div className={styles.field}>
                        <span>E-mail Institucional</span>
                        <input
                            className={styles.email}
                            type="email"
                            id="emailAluno"
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
