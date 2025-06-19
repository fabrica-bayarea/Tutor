import logging
from application.config.vector_database import chroma_client
from langchain_community.embeddings import HuggingFaceEmbeddings

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGEngine:
    def __init__(self, collection_name: str = "documentos"):
        """
        Inicializa o motor RAG com o banco de vetores ChromaDB existente.
        
        Espera receber:
            - `collection_name`: Nome da coleção ChromaDB a ser usada
        """
        logger.info(f"Inicializando RAGEngine com coleção: '{collection_name}'")
        
        # Usa o mesmo modelo de embeddings que já está sendo usado no projeto
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"  # Modelo com dimensão 384
        )
        
        try:
            # Obtém a coleção usando o cliente ChromaDB existente
            self.collection = chroma_client.get_collection(name=collection_name)
            logger.info(f"Coleção '{collection_name}' carregada com sucesso")
            
            # Verifica se há documentos na coleção
            count = self.collection.count()
            logger.info(f"Documentos na coleção: {count}")
            
            # Importa o Chroma do LangChain para usar com os embeddings
            from langchain_community.vectorstores import Chroma
            
            # Cria uma instância do Chroma do LangChain usando o cliente existente
            self.vector_db = Chroma(
                client=chroma_client,
                collection_name=collection_name,
                embedding_function=self.embeddings
            )
            
        except Exception as e:
            logger.error(f"Erro ao acessar o banco de vetores: {str(e)}")
            raise RuntimeError(f"Erro ao acessar o banco de vetores: {e}")

    def retrieve(self, query: str, k: int = 4) -> list[str]:
        """
        Recupera os k documentos mais relevantes para a consulta.
        
        Espera receber:
            - `query`: Texto da consulta
            - `k`: Número de documentos a retornar
            
        Retorna uma lista de trechos de documentos relevantes
        """
        try:
            logger.info(f"Buscando documentos relevantes para: '{query}'")
            
            # Usa o método similarity_search do LangChain
            docs = self.vector_db.similarity_search(query, k=k)
            
            # Log dos documentos encontrados
            for i, doc in enumerate(docs):
                logger.info(f"Documento {i+1} - Metadados: {doc.metadata}")
                logger.info(f"Conteúdo: {doc.page_content[:200]}..." if doc.page_content else "[SEM CONTEÚDO]")
                
            return [doc.page_content for doc in docs] if docs else []
            
        except Exception as e:
            logger.error(f"Erro ao recuperar documentos: {str(e)}")
            return []

    def build_prompt(self, query: str, context: list[str]) -> str:
        """
        Constrói o prompt para o LLM com base na consulta e contexto.
        
        Espera receber:
            - `query`: Consulta do usuário
            - `context`: Lista de trechos relevantes
            
        Retorna o prompt formatado
        """
        logger.info(f"Construindo prompt para a pergunta: '{query}'")
        logger.info(f"Número de contextos recebidos: {len(context)}")
        
        if not context:
            logger.warning("Nenhum contexto foi fornecido para construir o prompt")
            return f"Pergunta: {query}\n\nResposta: Não encontrei informações relevantes nos documentos para responder a esta pergunta."
            
        context_text = "\n\n".join([f"Trecho {i+1}: {doc}" for i, doc in enumerate(context)])
        
        prompt = f"""Com base APENAS nas informações fornecidas nos trechos abaixo, responda à pergunta do usuário.
Se a resposta não estiver contida NOS TREXOS FORNECIDOS, responda APENAS "Não sei responder com base nas informações disponíveis".

Trechos de documentos:
{context_text}

Pergunta: {query}

Resposta:"""
        
        logger.debug(f"Prompt gerado:\n{prompt}")
        return prompt
