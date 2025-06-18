from rag_engine import RAGEngine


class RAGPipeline:
    def __init__(self, rag:RAGEngine, LLMWrapper):
        """
        Inicializa o pipeline RAG com os componentes de recuperação e geração.

        Espera receber:

        rag: RAGEngine - mecanismo de recuperação de contexto.
        llm: LLWrapper - modelo de linguagem para geração de resposta.
        """

        self.rag = rag
        self.llm = LLMWrapper
        
    def responder(self, pergunta: str, k: int = 3) -> str:
        """
        Processa uma pergunta realizando recuperação de contexto e geração de resposta.

        Espera receber:
        
        pergunta: str - a pergunta feita pelo usuário.
        k: int - número de documentos relevantes a recuperar (padrão: 3)

        Retorna:
        
        str - a resposta gerada pela LLM baseada nos documentos recuperados."""
        contextos = self.rag.recuperar_contexto(pergunta, k=k)
        contexto = "\n".join(contextos)
        prompt = self.rag.build_prompt(pergunta, contexto)
        resposta = self.llm.generate(prompt)
        return resposta