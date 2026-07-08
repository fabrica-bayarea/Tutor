"""
Configuração do banco vetorial usando pgvector (extensão do PostgreSQL).

Substitui o ChromaDB embarcado por uma tabela no RDS compartilhado, usando
a extensão `vector` para busca semântica por similaridade de cosseno.

A tabela `documento_vetor` armazena os embeddings e metadados de cada documento
indexado. Os embeddings são gerados pelo modelo sentence-transformers local
(all-MiniLM-L6-v2, 384 dimensões) — o mesmo que o ChromaDB usava internamente.
"""
from application.config.database import db
from pgvector.sqlalchemy import Vector
from sqlalchemy import Index


# Dimensão do modelo all-MiniLM-L6-v2 (padrão do ChromaDB)
EMBEDDING_DIM = 384


class DocumentoVetor(db.Model):
    """Tabela de documentos vetorizados para busca semântica (RAG)."""
    __tablename__ = "documento_vetor"
    __table_args__ = {"schema": "tutor"}

    id = db.Column(db.String(36), primary_key=True)
    arquivo_id = db.Column(db.String(36), nullable=False, index=True)
    titulo = db.Column(db.String(512), nullable=True)
    professor_id = db.Column(db.String(36), nullable=True)
    vinculos = db.Column(db.Text, nullable=True)
    tipo = db.Column(db.String(50), nullable=True)
    data_upload = db.Column(db.DateTime, nullable=True)
    conteudo = db.Column(db.Text, nullable=False)
    embedding = db.Column(Vector(EMBEDDING_DIM), nullable=False)


# Índice IVFFlat para busca vetorial eficiente por cosseno
Index(
    "ix_documento_vetor_embedding",
    DocumentoVetor.embedding,
    postgresql_using="ivfflat",
    postgresql_with={"lists": 100},
    postgresql_ops={"embedding": "vector_cosine_ops"},
)
