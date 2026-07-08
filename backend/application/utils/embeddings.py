"""
Geração de embeddings para busca vetorial.

Usa o modelo all-MiniLM-L6-v2 (384 dimensões) via sentence-transformers —
o mesmo modelo padrão que o ChromaDB utilizava internamente.

O modelo é carregado uma única vez (singleton) para evitar reload a cada chamada.
"""
from sentence_transformers import SentenceTransformer

_model = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def gerar_embedding(texto: str) -> list[float]:
    """Gera embedding de um texto. Retorna lista de 384 floats."""
    model = _get_model()
    return model.encode(texto, normalize_embeddings=True).tolist()


def gerar_embeddings_batch(textos: list[str]) -> list[list[float]]:
    """Gera embeddings para uma lista de textos."""
    model = _get_model()
    return model.encode(textos, normalize_embeddings=True).tolist()
