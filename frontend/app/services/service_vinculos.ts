import api from "./api";
import { InterfaceAlunoTurma, InterfaceTurmaMateria, InterfaceProfessorTurmaMateria, InterfaceArquivoTurmaMateria } from "../types";

const vinculos_url = "vinculos";

// -------------------- ALUNO <-> TURMA --------------------

export async function obterVinculosAlunoTurma(aluno_id: string) {
    try {
        const response: { data: InterfaceAlunoTurma[] } = await api.get(`/${vinculos_url}/alunos_turmas/aluno/${aluno_id}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar os vínculos aluno_turma:", error);
        throw error;
    }
}

// -------------------- TURMA <-> MATÉRIA --------------------

export async function obterVinculosTurmaMateria(turma_id: string) {
    try {
        const response: { data: InterfaceTurmaMateria[] } = await api.get(`/${vinculos_url}/turmas_materias/turma/${turma_id}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar os vínculos turma_materia:", error);
        throw error;
    }
}

// -------------------- PROFESSOR <-> TURMA <-> MATÉRIA --------------------

export async function obterVinculosProfessorTurmaMateria(professor_id: string) {
    try {
        const response: { data: InterfaceProfessorTurmaMateria[] } = await api.get(`/${vinculos_url}/professores_turmas_materias/professor/${professor_id}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar os vínculos professor_turma_materia:", error);
        throw error;
    }
}

// -------------------- ARQUIVO <-> TURMA <-> MATÉRIA --------------------

export async function obterVinculosArquivoTurmaMateria(turma_id: string, materia_id: string) {
    try {
        const response: { data: InterfaceArquivoTurmaMateria[] } = await api.get(`/${vinculos_url}/arquivos_turmas_materias/${turma_id}_${materia_id}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar os vínculos arquivo_turma_materia:", error);
        throw error;
    }
}
