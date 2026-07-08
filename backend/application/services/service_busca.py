from application.config.database import db
from application.config.vector_database import DocumentoVetor
from application.utils.embeddings import gerar_embedding


def executar_busca_semantica(mensagem_usuario: str, arquivos_ids: list[str]) -> list[dict]:
    """
    Executa busca semântica no pgvector filtrando pelos IDs dos arquivos
    vinculados à matéria e retorna os trechos formatados para o prompt LLM.
    """
    if not arquivos_ids:
        return [{"role": "system", "content": "Nenhum arquivo vinculado a esta matéria."}]

    query_embedding = gerar_embedding(mensagem_usuario)
    resultados = (
        db.session.query(DocumentoVetor.conteudo)
        .filter(DocumentoVetor.arquivo_id.in_(arquivos_ids))
        .order_by(DocumentoVetor.embedding.cosine_distance(query_embedding))
        .limit(5)
        .all()
    )

    documentos = [r.conteudo for r in resultados if r.conteudo]

    if not documentos:
        return [{"role": "system", "content": "Nenhum trecho relevante encontrado."}]

    return [{"role": "system", "content": trecho} for trecho in documentos]
