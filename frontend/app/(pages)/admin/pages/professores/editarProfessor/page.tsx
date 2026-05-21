"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import FormularioProfessor from "../../../components/FormularioProfessor/FormularioProfessor";

function EditarProfessorContent() {
    const searchParams = useSearchParams();
    const id = searchParams?.get("id") ?? "";
    const nome = searchParams?.get("nome") ?? "";
    const matricula = searchParams?.get("matricula") ?? "";
    const email = searchParams?.get("email") ?? "";

    return (
        <div>
            <FormularioProfessor
                mode={"editarProfessor"}
                initialId={id}
                initialNome={nome}
                initialMatricula={matricula}
                initialEmail={email}
            />
        </div>
    );
}

export default function EditarProfessor() {
    return (
        <Suspense fallback={<div>Carregando...</div>}>
            <EditarProfessorContent />
        </Suspense>
    );
}
