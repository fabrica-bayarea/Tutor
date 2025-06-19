import logging

# Configuração básica de logging
logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, rag, llm):
        """
        Inicializa o pipeline RAG com os componentes de recuperação e geração.

        Espera receber:
            - `rag`: Instância do RAGEngine para recuperação de contexto
            - `llm`: Instância do LLMWrapper para geração de respostas
        """
        self.rag = rag
        self.llm = llm
        logger.info("Pipeline RAG inicializado com sucesso")
        
    def run(self, query: str, k: int = 4) -> str:
        """
        Processa uma pergunta, recupera contexto relevante e gera uma resposta.

        Espera receber:
            - `query`: A pergunta do usuário
            - `k`: Número de trechos relevantes a recuperar
            
        Retorna a resposta gerada pelo modelo
        """
        logger.info(f"Processando pergunta: '{query}'")
        
        try:
            # Recupera os contextos relevantes
            logger.info("Buscando contextos relevantes...")
            contextos = self.rag.retrieve(query, k=k)
            
            if not contextos:
                logger.warning("Nenhum contexto relevante encontrado")
                return "Não foi possível encontrar informações relevantes nos documentos."
            
            # Constrói o prompt com a pergunta e os contextos
            logger.info("Construindo prompt...")
            prompt = self.rag.build_prompt(query, contextos)
            
            # Gera a resposta usando o LLM
            logger.info("Gerando resposta...")
            resposta = self.llm.generate(prompt)
            
            logger.info("Resposta gerada com sucesso")
            return resposta
            
        except Exception as e:
            error_msg = f"Erro ao processar a pergunta: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return error_msg
