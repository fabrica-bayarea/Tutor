import asyncio

from typing import List
from application.config.database import db
from application.config.vector_database import collection
from application.models import ArquivoTurmaMateria
from application.socket.Impl.disparar_emit import disparar_emit

def obter_arquivos_por_materia(materia_id:str) -> List[str]:

    registros = db.session.query(ArquivoTurmaMateria).filter_by(materia_id=materia_id).all()
    return [str(registros_encontrados.arquivo_id) for registros_encontrados in registros]

def buscar_no_vector_db(query: str, arquivos_ids: List[str], top_k: int = 5) -> List[str]:

    if not arquivos_ids: return []

    try:
        resultados = collection.query(
            query_texts=[query],
            where={"arquivo_id": {"$in": arquivos_ids}},
            n_results=top_k
        )

        documentos = resultados.get("documents", [[]])[0]

        if not documentos: return []

        return [documento_encontrado.strip() for documento_encontrado in documentos if documento_encontrado]
    
    except Exception:
        return []

def formatar_para_rag(chunks:List[str]) -> List[str]:

    if not chunks: return[]

    seen = set()
    resultado = []

    for chunk in chunks:
        if chunk not in seen:
            seen.add(chunk)
            resultado.append(chunk)
    
    return resultado

async def busca_semantica(materia_id:str,query:str,sid,socketio) -> List[str]:
    
    disparar_emit(socketio, 'buscando_arquivos',{}, room=sid)

    arquivos_ids = await asyncio.to_thread(
        obter_arquivos_por_materia,
        materia_id
    )

    if not arquivos_ids: return ""

    disparar_emit(socketio, 'buscando_vetores',{}, room=sid)
    chunks = await asyncio.to_thread(buscar_no_vector_db(query,arquivos_ids))

    disparar_emit(socketio, 'formatando_chunks',{}, room=sid)
    return formatar_para_rag(chunks)
