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

        const response: { data: InterfaceUploadResponse } = await api.post(`/${arquivos_url}/upload/arquivos`, formData);

        return response.data;
    } catch (error) {
        console.error("Erro ao processar o(s) arquivo(s):", error);
        throw error;
    }
}

export async function uploadLinks(urls: string[], vinculos: InterfaceTurmaMateria[]) {
    try {
        const response: { data: InterfaceUploadResponse } = await api.post(`/${arquivos_url}/upload/links`, { urls, vinculos });

        return response.data;
    } catch (error) {
        console.error("Erro ao processar o(s) link(s):", error);
        throw error;
    }
}

export async function uploadTextos(textos: string[], vinculos: InterfaceTurmaMateria[]) {
    try {
        const response: { data: InterfaceUploadResponse } = await api.post(`/${arquivos_url}/upload/textos`, { textos, vinculos });

        return response.data;
    } catch (error) {
        console.error("Erro ao processar o(s) texto(s):", error);
        throw error;
    }
}

export async function getArquivos(turma_id: string, materia_id: string) {
    try {
        const response: { data: InterfaceArquivo[] } = await api.get(`/${arquivos_url}/${turma_id}_${materia_id}`);

        return response.data;
    } catch (error) {
        console.error("Erro ao obter os arquivos:", error);
        throw error;
    }
}

export async function getDownloadArquivo(arquivo_id: string) {
    try {
        const response = await api.get(`/${arquivos_url}/download/${arquivo_id}`)
        return response.data;
    } catch (error) {
        console.error("Erro ao baixar o arquivo:", error);
        throw error;
    }
}