from chromadb import PersistentClient
import os

CHROMADB_PATH = "/data/chroma"
os.makedirs(CHROMADB_PATH, exist_ok=True)

chroma_client = PersistentClient(path=CHROMADB_PATH)
collection = chroma_client.get_or_create_collection(name="documentos")
