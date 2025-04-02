import os
import uuid
from datetime import datetime
from typing import List
from config import db, chroma_client
from models import Documento
from libs.docling_handler import *

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DOCUMENTOS_DIR = os.path.join(BASE_DIR, "data/documentos")

def salvar_metadados_documento(titulo: str, professor_id: uuid.UUID) -> Documento:
    """
    Salva metadados do documento no PostgreSQL.
    
    Retorna a estrutura completa do documento gerado, para uso posterior.
    """
    novo_documento = Documento(
        titulo=titulo,
        professor_id=professor_id
    )
    db.session.add(novo_documento)
    db.session.commit()
    return novo_documento

def salvar_arquivo(arquivo, documento_id: uuid.UUID, professor_id: uuid.UUID):
    """
    Salva o arquivo recebido no diretório do professor e retorna seu caminho.
    """
    if not os.path.exists(DOCUMENTOS_DIR):
        os.makedirs(DOCUMENTOS_DIR)
    
    diretorio_professor = os.path.join(DOCUMENTOS_DIR, str(professor_id))
    
    if not os.path.exists(diretorio_professor):
        os.makedirs(diretorio_professor)
    
    nome_original = arquivo.filename
    nome_arquivo = f"{documento_id}_{nome_original}"
    caminho_arquivo = os.path.join(diretorio_professor, nome_arquivo)

    arquivo.save(caminho_arquivo)
    
    return caminho_arquivo

def salvar_documento_vetor(documento_id: uuid.UUID, titulo: str, professor_id: uuid.UUID, materia_ids: List[uuid.UUID], timestamp: datetime, texto: str):
    """
    Salva dados do documento no ChromaDB.
    """
    collection = chroma_client.get_or_create_collection("documentos")
    collection.add(
        id=[str(documento_id)],
        metadatas=[{
            "titulo": titulo,
            "professor_id": str(professor_id),
            "materia_ids": [str(materia_id) for materia_id in materia_ids],
            "tipo": "pdf",
            "data_upload": timestamp.isoformat(),
        }],
        conteudo=[texto]
    )

def processar_documento(arquivo, professor_id: uuid.UUID, materia_ids: List[uuid.UUID]):
    """
    Processa um documento:
    
    1. Salva metadados no PostgreSQL
    2. Salva o arquivo recebido no diretório do professor
    3. Extrai o conteúdo via Docling
    4. Indexa no ChromaDB utilizando o mesmo ID do PostgreSQL.

    Retorna um dicionário com informações do documento.
    """
    # 1. Salva metadados no PostgreSQL e retorna a estrutura completa do documento
    nome_arquivo = arquivo.filename
    documento = salvar_metadados_documento(nome_arquivo, professor_id)

    # 2. Salva o arquivo no diretório do professor e retorna o caminho para ele
    # Usa o ID retornado na etapa anterior
    caminho_arquivo = salvar_arquivo(arquivo, documento.id, professor_id)
    
    # 3. Extrai o texto em Markdown usando Docling
    # Usa o caminho retornado na etapa anterior
    texto_extraido = extrair_texto_markdown(caminho_arquivo)
    
    # 4. Salva o documento no ChromaDB
    salvar_documento_vetor(documento.id, documento.titulo, professor_id, materia_ids, documento.timestamp, texto_extraido)
    
    return {"documento_id": documento.id, "titulo": nome_arquivo}
