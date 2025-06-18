import os
import torch

from typing import List
from sentence_transformers import SentenceTransformer
from langchain.community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader


class RAGengine:
    def __init__(self, embendding_model_name: str = "sentence-tranformers/all-mpnet-base-v2", persist_directory: str = "chromba_db"):       
        """
        Inicializa o mecanismo de RAG (Retrieval-Augmented Generation).

        Espera receber:
        - `embedding_model_name`: str - o nome do modelo de embeddings da `sentence-transformers`.
        - `persist_directory`: str - o diretório onde os vetores serão armazenados pelo ChromaDB.

        Configura o modelo de embeddings e prepara a estrutura para armazenamento vetorial.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.embbending_model = SentenceTransformer(embendding_model_name, device = self.device)
        self.vectorstore = None
        self.persist_directory = persist_directory
    
    def load_documents(self, data_dir: str, chunk_size: int = 512, chunk_overlap: int = 50):
        """
        Carrega documentos .pdf e .txt de um diretório, gera embeddings e os armazena no ChromaDB.

        Espera receber:
        - `data_dir`: str - o caminho do diretório onde os arquivos estão localizados.
        - `chunk_size`: int - o tamanho máximo de cada pedaço de texto (default: 512).
        - `chunk_overlap`: int - o número de tokens de sobreposição entre os pedaços (default: 50).

        Cria o vetorstore persistente com os textos embeddados.
        """
          
        loaders = []
        
        for root, _, files in os.walk(data_dir):
            for file in files:
                path = os.path.join(root, file)
                if file.lower().endswith('.pdf'):
                    loaders.append(PyPDFLoader(path))
                elif file.lower().endswith('.txt'):
                    loaders.append(TextLoader(path, encoding="utf-8"))
                    
        documents = []
        for loader in loaders:
            documents.extend(loader.load())
            
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(documents)
        
        self.vectorstore = Chroma.from_documents(
            documents = chunks,
            embedding = self.embbending_model,
            persist_directory = self.persist_directory
        )

        self.vectorstore.persist()
            
    def retrive(self, query: str, k: int = 3) -> List[str]:
        """
        Recupera os documentos mais relevantes a partir de uma consulta textual.

        Espera receber:
        - `query`: str - a pergunta ou termo de busca.
        - `k`: int - a quantidade de documentos a retornar (default: 3).

        Retorna uma lista de strings com os conteúdos mais relevantes. Caso nenhum vetorstore tenha sido carregado, retorna uma mensagem de aviso..
        """
        
        if self.vectorstore is None:
            return ["Nenhum documento foi carregado ainda. Por favor, envie um arquivo primeiro."]
            
        docs = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
    
    def build_prompt(self, question: str, context: str) -> str:
        """
        Constrói o prompt a ser passado para o modelo de linguagem, com base no contexto e na pergunta.

        Espera receber:
        - `question`: str - a pergunta feita pelo usuário.
        - `context`: str - o conteúdo extraído dos documentos para embasar a resposta.

        Retorna o prompt formatado no estilo: "Contexto...\n\nPergunta...\n\nResposta:"
        """
        
        return f"Contexto: {context}\n\nPergunta: {question}\n\nResposta:"