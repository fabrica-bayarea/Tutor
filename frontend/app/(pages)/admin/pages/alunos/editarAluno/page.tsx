"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import FormularioAluno from "../../../components/FormularioAluno/FormularioAluno";

function EditarAlunoContent() {
    const searchParams = useSearchParams();
    const nome = searchParams?.get("nome") ?? "";
    const matricula = searchParams?.get("matricula") ?? "";
    const email = searchParams?.get("email") ?? "";

    return (
        <div>
            <FormularioAluno
                mode={"editarAluno"}
                initialNome={nome}
                initialMatricula={matricula}
                initialEmail={email}
            />
        </div>
    );
}

export default function EditarAluno() {
    return (
        <Suspense fallback={<div>Carregando...</div>}>
            <EditarAlunoContent />
        </Suspense>
    );
}
