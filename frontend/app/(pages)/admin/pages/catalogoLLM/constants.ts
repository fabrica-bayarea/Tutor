export type ModeloCatalogo = {
    nome: string;
    descricao: string;
    tamanho: string;
};

// Catálogo curado dos modelos conhecidos (nome no Ollama, descrição e tamanho
// aproximado). É exibido na tabela mesmo antes de instalado; o estado real
// (instalado / baixando / ativo) vem da API e é cruzado por `nome`. Espelha o
// protótipo do Figma (US-38.5).
export const CATALOGO_LLM: ModeloCatalogo[] = [
    { nome: "llama3.2:3b", descricao: "Meta LLaMA 3.2 • 3B parâmetros", tamanho: "2,0 GB" },
    { nome: "gemma3:4b", descricao: "Google Gemma 3 • 4B parâmetros", tamanho: "3,3 GB" },
    { nome: "mistral:7b", descricao: "Mistral AI • 7B parâmetros", tamanho: "4,1 GB" },
    { nome: "deepseek-r1:7b", descricao: "DeepSeek R1 • 7B parâmetros", tamanho: "4,7 GB" },
    { nome: "phi4:14b", descricao: "Microsoft Phi-4 • 14B parâmetros", tamanho: "9,1 GB" },
];

// Linha já resolvida para a tabela: dados do catálogo + situação na API.
export type LinhaModelo = {
    nome: string;
    descricao: string;
    tamanho: string;
    id: string | null; // id na API quando o modelo já foi cadastrado
    cadastrado: boolean;
    ativo: boolean;
};

// Mensagens de feedback com os textos exatos do protótipo do Figma (US-38.5).
export const MSG = {
    listaErro:
        "Não foi possível carregar a lista de modelos. Verifique a conexão e tente novamente.",
    ollamaIndisponivel:
        "Serviço Ollama não encontrado. Verifique se o Ollama está em execução.",
    falhaDownload: (nome: string) =>
        `Falha ao baixar o modelo ${nome}. Verifique a conexão e tente novamente.`,
    falhaAdicionar: (nome: string) =>
        `Falha ao adicionar o modelo ${nome}. Verifique o modelo e tente novamente.`,
    downloadIniciado: (nome: string) => `Download de ${nome} iniciado.`,
    ativadoSucesso: (nome: string) => `Modelo ${nome} ativado com sucesso.`,
};
