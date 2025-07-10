import api from "./api";
import { InterfaceMensagem } from "../types";

const mensagens_url = "mensagens";

export async function obterMensagens(chat_id: string) {
    try {
        const response: { data: InterfaceMensagem[] } = await api.get(`/${mensagens_url}/chat/${chat_id}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar mensagens:", error);
        throw error;
    }
}
