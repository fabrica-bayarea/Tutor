from chromadb import PersistentClient
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
CHROMADB_PATH = os.path.join(BASE_DIR, "data/chromadb")

os.makedirs(CHROMADB_PATH, exist_ok=True)

chroma_client = PersistentClient(path=CHROMADB_PATH)
