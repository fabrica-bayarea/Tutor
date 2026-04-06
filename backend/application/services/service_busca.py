from application.config.vector_database import collection

def executar_busca_semantica(mensagem_usuario: str, arquivos_ids: list[str]) -> list[dict]:
    """
    Executa busca semântica no ChromaDB filtrando pelos IDs dos arquivos
    vinculados à matéria e retorna os trechos formatados para o prompt LLM.
    """
    if not arquivos_ids:
        return [{"role": "system", "content": "Nenhum arquivo vinculado a esta matéria."}]

    resultados = collection.query(
        query_texts=[mensagem_usuario],
        where={"id": {"$in": arquivos_ids}},
        n_results=5
    )

    documentos = resultados.get("documents", [[]])[0]

    if not documentos:
        return [{"role": "system", "content": "Nenhum trecho relevante encontrado."}]

    return [{"role": "system", "content": trecho} for trecho in documentos]