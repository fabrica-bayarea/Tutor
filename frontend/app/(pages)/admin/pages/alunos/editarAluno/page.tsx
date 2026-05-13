"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import FormularioAluno from "../../../components/FormularioAluno/FormularioAluno";

function EditarAlunoContent() {
    const searchParams = useSearchParams();
    const id = searchParams?.get("id") ?? "";
    const nome = searchParams?.get("nome") ?? "";
    const matricula = searchParams?.get("matricula") ?? "";
    const email = searchParams?.get("email") ?? "";

    return (
        <div>
            <FormularioAluno
                mode={"editarAluno"}
                initialId={id}
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
