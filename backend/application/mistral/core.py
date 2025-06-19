import os
from .rag_engine import RAGEngine
from .llm_load import LLMWrapper
from .rag_pipeline import RAGPipeline

# Caminhos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMA_DB_DIR = os.path.join(BASE_DIR, 'data', 'chromadb')

# Inicializa os componentes com o modelo local do Ollama
rag = RAGEngine(collection_name="documentos")  # Usa a coleção 'documentos' que já existe
llm = LLMWrapper(model_name="mistral")  # Usando o modelo mistral do Ollama
pipeline = RAGPipeline(rag=rag, llm=llm)

# Exemplo de uso
if __name__ == "__main__":
    try:
        # Testa a recuperação
        query = "Sobre o que são estes documentos?"
        print(f"Pergunta: {query}")
        
        # Executa o pipeline
        response = pipeline.run(query)
        print(f"Resposta: {response}")
        
    except Exception as e:
        print(f"Erro ao executar o pipeline: {str(e)}")
