"use client";

import { createContext, useEffect, useState } from "react";
import { buscar_materias_usuario, buscar_turmas_usuario } from "@/app/services/service_data";
import { useAuth } from "@/utils/auth";

interface materia {
    id: number,
    nome: string
}

interface turma {
    id: number,
    codigo: string,
    semestre: string,
    turno: string
}

interface DataContextType {
    materias: materia[];
    turmas: turma[];
}

export const DataContext = createContext<DataContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [materias, setMaterias] = useState<materia[]>([]);
    const [turmas, setTurmas] = useState<turma[]>([]);
    const { user } = useAuth();

    async function getData(){
        if (!user?.id) return;
        setMaterias(await buscar_materias_usuario(user?.id));
        setTurmas(await buscar_turmas_usuario(user?.id));
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
