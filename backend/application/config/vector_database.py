from chromadb import PersistentClient
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
CHROMADB_PATH = os.path.join(BASE_DIR, "data/chromadb")

os.makedirs(CHROMADB_PATH, exist_ok=True)

chroma_client = PersistentClient(path=CHROMADB_PATH)
collection = chroma_client.get_or_create_collection(name="documentos")
"""
Coleção com nome "documentos", para realizar todas as operações CRUD envolvendo vetores de documentos, como por exemplo:
- Criar novos vetores de documentos
- Fazer buscas semânticas de documentos
- Atualizar vetores de documentos
- Excluir vetores de documentos
"""
