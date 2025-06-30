import api from "./api";

const aluno_auth_url = "alunos";

async function postAlunoAuth(matricula_aluno: string, senha: string){
    try {
        const conteudo = {
            "matricula": matricula_aluno,
            "senha": senha
        };
        const response = await api.post(`${aluno_auth_url}/login`, conteudo, {
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                // "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        });
        return response.data;
    } catch (error) {
        console.error("Erro ao autenticar o aluno:", error);
        throw error;
    }
}

export { postAlunoAuth };