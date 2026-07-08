import asyncio
from typing import List

from application.config.database import db
from application.config.vector_database import DocumentoVetor
from application.models import ArquivoTurmaMateria
from application.utils.embeddings import gerar_embedding


def obter_arquivos_por_materia(materia_id: str) -> List[str]:
    registros = db.session.query(ArquivoTurmaMateria).filter_by(materia_id=materia_id).all()
    return [str(r.arquivo_id) for r in registros]


def buscar_no_vector_db(query: str, arquivos_ids: List[str], top_k: int = 5) -> List[str]:
    """Busca semântica via pgvector usando similaridade de cosseno."""
    if not arquivos_ids:
        return []

    try:
        query_embedding = gerar_embedding(query)
        resultados = (
            db.session.query(DocumentoVetor.conteudo)
            .filter(DocumentoVetor.arquivo_id.in_(arquivos_ids))
            .order_by(DocumentoVetor.embedding.cosine_distance(query_embedding))
            .limit(top_k)
            .all()
        )
        return [r.conteudo.strip() for r in resultados if r.conteudo]
    except Exception:
        return []


def formatar_para_rag(chunks: List[str]) -> List[str]:
    if not chunks:
        return []

    seen = set()
    resultado = []
    for chunk in chunks:
        if chunk not in seen:
            seen.add(chunk)
            resultado.append(chunk)
    return resultado


async def busca_semantica(materia_id: str, query: str) -> List[str]:
    arquivos_ids = await asyncio.to_thread(obter_arquivos_por_materia, materia_id)
    if not arquivos_ids:
        return ""
    chunks = await asyncio.to_thread(buscar_no_vector_db, query, arquivos_ids)
    return formatar_para_rag(chunks)
