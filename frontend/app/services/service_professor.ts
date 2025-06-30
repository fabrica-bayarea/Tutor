import api from "./api";

const professor_auth_url = "professores";

async function postProfessorAuth(matricula_professor: string, senha: string){
    try {
        const conteudo = {
            "matricula": matricula_professor,
            "senha": senha
        };
        const response = await api.post(`${professor_auth_url}/login`, conteudo, {
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                // "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        });
        return response.data;
    } catch (error) {
        console.error("Erro ao autenticar o professor:", error);
        throw error;
    }
}

export { postProfessorAuth };