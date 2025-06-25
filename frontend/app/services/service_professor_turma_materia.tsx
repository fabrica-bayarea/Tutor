import api from "./api";

const professores_turma_materia_url = "professores";

async function getVinculosProfessorTurmaMateria(matricula_professor: string) {
    try {
        const response = await api.get(`/${professores_turma_materia_url}/turmas_materias/${matricula_professor}`);
        const vinculos = response.data.map((vinculo: any) => ({
            ...vinculo,
            classCode: vinculo.codigo_turma,
            subjectCode: vinculo.codigo_materia,
        }));
        return vinculos;
    } catch (error) {
        console.error("Erro ao buscar os vínculos do professor:", error);
        throw error;
    }
}

export { getVinculosProfessorTurmaMateria };
