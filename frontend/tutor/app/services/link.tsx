import axios from "axios";

const linkAPI = axios.create({baseURL: 'http://127.0.0.1:5000/links', timeout: 30000})

async function postLinks(links: string[]) {
    try {
        const payload = links.length === 1 ? { "url": links[0] } : { "urls": links };
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