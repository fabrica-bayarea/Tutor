import os
from .rag_engine import RAGEngine
from .llm_load import LLMWrapper
from .rag_pipeline import RAGPipeline

# Caminhos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMA_DB_DIR = os.path.join(BASE_DIR, 'data', 'chromadb')

# Variáveis globais
rag = None
llm = None
pipeline = None

def initialize_all():
    """
    Inicializa o mecanismo de busca vetorial (RAG), o wrapper do modelo (LLM)
    e a pipeline que integra ambos.
    """
    global rag, llm, pipeline

    if rag and llm and pipeline:
        return  # Já inicializado

    print("[CORE] Inicializando RAG Engine...")
    rag = RAGEngine(collection_name="documentos")

    print("[CORE] Inicializando LLMWrapper...")
    llm = LLMWrapper(model_name="mistral")

    print("[CORE] Inicializando RAGPipeline...")
    pipeline = RAGPipeline(rag=rag, llm=llm)

    print("[CORE] Sistema de RAG + LLM pronto para uso.")

# Executa automaticamente ao importar
initialize_all()

if __name__ == "__main__":
    try:
        query = "Sobre o que são estes documentos?"
        print(f"Pergunta: {query}")
        response = pipeline.run(query)
        print(f"Resposta: {response}")
    except Exception as e:
        print(f"[CORE] Erro ao executar o pipeline: {str(e)}")
