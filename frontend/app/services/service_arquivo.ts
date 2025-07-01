import api from "./api";
import { InterfaceArquivo, InterfaceTurmaMateria } from "../types";

interface InterfaceUploadResponse {
    message: string;
    results: {
        filename: string;
        status: number;
        data: InterfaceArquivo;
    }[];
}

const arquivos_url = "arquivos";

export async function uploadArquivos(arquivos: File[], vinculos: InterfaceTurmaMateria[]) {
    try {
        const formData = new FormData();
        
        arquivos.forEach((arquivo) => {
            formData.append('arquivos', arquivo);
        });

        formData.append('vinculos', JSON.stringify(vinculos));

        const response: InterfaceUploadResponse = await api.post(`/${arquivos_url}/upload/arquivos`, formData);
        console.log(response)

        return response;
    } catch (error) {
        console.error("Erro ao processar o(s) arquivo(s):", error);
        throw error;
    }
}

export async function uploadLinks(links: string[], vinculos: InterfaceTurmaMateria[]) {
    try {
        const response: InterfaceUploadResponse = await api.post(`/${arquivos_url}/upload/links`, { links, vinculos });
        console.log(response)

        return response;
    } catch (error) {
        console.error("Erro ao processar o(s) link(s):", error);
        throw error;
    }
}

export async function uploadTextos(textos: string[], vinculos: InterfaceTurmaMateria[]) {
    try {
        const response: InterfaceUploadResponse = await api.post(`/${arquivos_url}/upload/textos`, { textos, vinculos });
        console.log(response)

        return response;
    } catch (error) {
        console.error("Erro ao processar o(s) texto(s):", error);
        throw error;
    }
}

// export async function getArquivos(id_professor){
//     pass
// }
