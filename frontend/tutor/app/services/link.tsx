import axios from "axios";

const linkAPI = axios.create({baseURL: 'http://127.0.0.1:5000/links', timeout: 30000})

async function postLinks(links: string[], matricula_professor: string, viculos: any[]) {
    try {
        const payload = {
            "urls": links,
            "matricula_professor": matricula_professor,
            "vinculos": vinculos
        };
        const response = await linkAPI.post('/upload', payload, {
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        });
        return response.data;
    } catch (error) {
        console.error("Erro ao enviar os links:", error);
        throw error;
    }
}

export { postLinks };