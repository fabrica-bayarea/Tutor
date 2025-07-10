import api from "./api";
import { InterfaceChat } from "../types";

const chats_url = "chats";

export async function obterChats(aluno_id: string) {
    try {
        const response: { data: InterfaceChat[] } = await api.get(`/${chats_url}/aluno/${aluno_id}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar chats:", error);
        throw error;
    }
}

export async function atualizarChat(chat_id: string, novo_nome: string) {
    try {
        const response: { data: InterfaceChat } = await api.patch(`/${chats_url}/chat/${chat_id}`, { nome: novo_nome });
        return response.data;
    } catch (error) {
        console.error("Erro ao atualizar chat:", error);
        throw error;
    }
}

export async function deletarChat(chat_id: string) {
    try {
        const response: { data: InterfaceChat } = await api.delete(`/${chats_url}/chat/${chat_id}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao deletar chat:", error);
        throw error;
    }
}