import axios from "axios";

const professorTurmaMateriaAPI = axios.create({baseURL: 'http://127.0.0.1:5000/professores', timeout: 30000})

async function getVinculosProfessorTurmaMateria(matricula_professor: string) {
    try {
        const response = await professorTurmaMateriaAPI.get(`/turmas_materias/${matricula_professor}`);
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
