"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import FormularioMateria from "../../../components/FormularioMateria/FormularioMateria";

function EditarMateriaContent() {
    const searchParams = useSearchParams();
    const id = searchParams?.get("id") ?? "";
    const codigo = searchParams?.get("codigo") ?? "";
    const nome = searchParams?.get("nome") ?? "";
    const status = searchParams?.get("status") ?? "ATIVO";

    return (
        <div>
            <FormularioMateria
                mode={"editarMateria"}
                initialId={id}
                initialCodigo={codigo}
                initialNome={nome}
                initialStatus={status}
            />
        </div>
    );
}

export default function EditarMateria() {
    return (
        <Suspense fallback={<div>Carregando...</div>}>
            <EditarMateriaContent />
        </Suspense>
    );
}
