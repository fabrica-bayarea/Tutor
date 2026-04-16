"use client";

import { createContext, useEffect, useState } from "react";
import { buscar_materias_usuario, buscar_turmas_usuario } from "@/app/services/service_data";
import { useAuth } from "@/utils/auth";

interface materia {
    id: string,
    nome: string
}

interface turma {
    id: string,
    codigo: string,
    semestre: string,
    turno: string
}

interface DataContextType {
    materias: materia[];
    turmas: turma[];
}

export const DataContext = createContext<DataContextType | undefined>(undefined);

export function DataProvider({ children }: { children: React.ReactNode }) {
    const [materias, setMaterias] = useState<materia[]>([]);
    const [turmas, setTurmas] = useState<turma[]>([]);
    const { user } = useAuth();

    async function getData(){
        if (!user) return;
        setMaterias(await buscar_materias_usuario());
        setTurmas(await buscar_turmas_usuario());
    }


    useEffect(()=>{
        getData();
    },[user])

    return (
        <DataContext.Provider
            value={{
                materias,
                turmas
            }}
        >
            {children}
        </DataContext.Provider>
    );
}
