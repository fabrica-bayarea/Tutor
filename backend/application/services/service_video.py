import os
import uuid
from datetime import datetime
from application.config import db, chroma_client
from application.libs.whisper_handler import processar_video, transcrever_audio
from application.models import Documento

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
AUDIO_DIR = os.path.join(BASE_DIR, "data/audios")

def salvar_metadados_transcricao(titulo: str, professor_id: uuid.UUID) -> Documento:
    """
    Salva metadados da transcrição no PostgreSQL.
    """
    nova_transcricao = Documento(
        titulo=titulo,
        professor_id=professor_id
    )
    db.session.add(nova_transcricao)
    db.session.commit()
    return nova_transcricao

def salvar_audio(input_video: str, transcricao_id: uuid.UUID, professor_id: uuid.UUID) -> str:
    """
    Extrai e salva o áudio do vídeo no diretório do professor.
    """
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)
    
    diretorio_professor = os.path.join(AUDIO_DIR, str(professor_id))
    
    if not os.path.exists(diretorio_professor):
        os.makedirs(diretorio_professor)
    
    output_audio = os.path.join(diretorio_professor, f"{transcricao_id}.wav")
    processar_video(input_video, output_audio)
    
    return output_audio

def salvar_transcricao_vetor(transcricao_id: uuid.UUID, titulo: str, professor_id: uuid.UUID, timestamp: datetime, texto: str):
    """
    Salva a transcrição no ChromaDB.
    """
    collection = chroma_client.get_or_create_collection("transcricoes")
    collection.add(
        ids=[str(transcricao_id)],
        metadatas=[{
            "titulo": titulo,
            "professor_id": str(professor_id),
            "tipo": "transcricao",
            "data_upload": timestamp.isoformat(),
        }],
        documents=[texto]
    )

def processar_transcricao(input_video: str, professor_id: uuid.UUID):
    """
    Processa um vídeo:
    
    1. Salva metadados da transcrição no PostgreSQL
    2. Extrai e salva o áudio do vídeo
    3. Transcreve o áudio com Whisper
    4. Indexa a transcrição no ChromaDB
    
    Retorna um dicionário com informações da transcrição.
    """
    titulo = os.path.basename(input_video)
    transcricao = salvar_metadados_transcricao(titulo, professor_id)
    output_audio = salvar_audio(input_video, transcricao.id, professor_id)
    texto_transcrito = transcrever_audio(output_audio)
    salvar_transcricao_vetor(transcricao.id, transcricao.titulo, professor_id, transcricao.timestamp, texto_transcrito)
    
    return {"transcricao_id": transcricao.id, "titulo": titulo}