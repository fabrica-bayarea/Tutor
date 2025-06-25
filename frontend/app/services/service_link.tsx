import api from "./api";

const links_url = "links";

async function postLinks(links: string[], matricula_professor: string, vinculos: any[]) {
    try {
        const payload = {
            "urls": links,
            "matricula_professor": matricula_professor,
            "vinculos": vinculos
        };
        const response = await api.post(`/${links_url}/upload`, payload, {
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