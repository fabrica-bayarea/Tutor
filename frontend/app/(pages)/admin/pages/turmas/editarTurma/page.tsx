"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import FormularioTurma from "../../../components/FormularioTurma/FormularioTurma";

function EditarTurmaContent() {
    const searchParams = useSearchParams();
    const id = searchParams?.get("id") ?? "";
    const codigo = searchParams?.get("codigo") ?? "";
    const semestre = searchParams?.get("semestre") ?? "";
    const turno = searchParams?.get("turno") ?? "";
    const status = searchParams?.get("status") ?? "ATIVO";

    return (
        <div>
            <FormularioTurma
                mode={"editarTurma"}
                initialId={id}
                initialCodigo={codigo}
                initialSemestre={semestre}
                initialTurno={turno}
                initialStatus={status}
            />
        </div>
    );
}

export default function EditarTurma() {
    return (
        <Suspense fallback={<div>Carregando...</div>}>
            <EditarTurmaContent />
        </Suspense>
    );
}
