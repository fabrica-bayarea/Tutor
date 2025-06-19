import logging
from application.mistral.core import pipeline, rag

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def testar_pipeline():
    """Função para testar o pipeline RAG com informações detalhadas."""
    perguntas = [
        "Quais são minhas habilidades técnicas?",
        "Onde estudei?",
        "Quais são minhas experiências profissionais?"
    ]
    
    for pergunta in perguntas:
        print(f"\n{'='*80}")
        print(f"PERGUNTA: {pergunta}")
        print(f"{'='*80}")
        
        try:
            # Executa o pipeline
            resposta = pipeline.run(pergunta)
            
            # Exibe a resposta
            print(f"\nRESPOSTA: {resposta}")
            
        except Exception as e:
            print(f"\nERRO: {str(e)}")

if __name__ == "__main__":
    # Testa a conexão com o banco de vetores
    try:
        print("Verificando banco de vetores...")
        # Tenta acessar a coleção diretamente para verificar se há documentos
        collection = rag.vector_db._collection
        doc_count = collection.count()
        print(f"Total de documentos no banco de vetores: {doc_count}")
        
        if doc_count > 0:
            print("\nAmostra de documentos no banco:")
            sample = collection.get(limit=min(2, doc_count))
            for i, (doc_id, doc) in enumerate(zip(sample['ids'], sample['documents'])):
                print(f"\nDocumento {i+1} (ID: {doc_id}):")
                print(f"Conteúdo: {doc[:200]}...")
        else:
            print("AVISO: Nenhum documento encontrado no banco de vetores!")
            print("Certifique-se de que os documentos foram corretamente indexados.")
        
        # Executa os testes
        print("\n" + "="*80)
        print("INICIANDO TESTES DO PIPELINE")
        print("="*80)
        testar_pipeline()
        
    except Exception as e:
        print(f"ERRO AO ACESSAR O BANCO DE VETORES: {str(e)}")
