import os
import uuid
from datetime import datetime
from typing import List
from application.config import db, chroma_client
from application.models import Documento
from application.libs import *

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DOCUMENTOS_DIR = os.path.join(BASE_DIR, "data/documentos")

def salvar_metadados_arquivo(titulo: str, professor_id: uuid.UUID) -> Documento:
    """
    Salva metadados do documento no PostgreSQL.

    Espera receber:
    - `titulo`: str - o nome do arquivo
    - `professor_id`: uuid.UUID - o ID do professor

    Retorna a estrutura completa do documento gerado para uso posterior.
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
        ids=[str(documento_id)],
        metadatas=[{
            "titulo": titulo,
            "professor_id": str(professor_id),
            "materia_ids": ",".join([str(materia_id) for materia_id in materia_ids]), # Concatena os IDs das matérias numa única string, separando-os com vírgulas
            "tipo": "pdf",
            "data_upload": timestamp.isoformat(),
        }],
        documents=[texto]
    )

    print(f'\nDOCUMENTO SALVO NO CHROMADB COM SUCESSO!')

def processar_arquivo(arquivo, professor_id: uuid.UUID, materia_ids: List[uuid.UUID]):
    """
    Processa um arquivo.
    
    Espera receber:
    - `arquivo`: File - o arquivo a ser processado
    - `professor_id`: uuid.UUID - o ID do professor
    - `materia_ids`: List[uuid.UUID] - os IDs das matérias

    1. Salva metadados no PostgreSQL
    2. Salva o arquivo recebido no diretório do professor
    3. Extrai o conteúdo do arquivo utilizando a biblioteca correta de acordo com a sua extensão (PDF, DOCX, MP4, etc)
    4. Indexa no ChromaDB utilizando o mesmo ID do PostgreSQL

    Retorna um dicionário com informações do documento.
    """
    print(f'\n\nIniciando processamento do arquivo: {arquivo.filename}')

    # 1. Salva metadados no PostgreSQL e retorna a estrutura completa do documento
    print(f'\n(1/4). Salvando metadados do documento no PostgreSQL')
    nome_arquivo = arquivo.filename
    documento = salvar_metadados_arquivo(nome_arquivo, professor_id)
    print(f'DADOS SALVOS NO POSTGRESQL COM SUCESSO!')

    # 2. Salva o arquivo no diretório do professor e retorna o caminho para ele
    # Usa o ID retornado na etapa anterior
    print(f'\n(2/4). Salvando arquivo no diretório do professor')
    caminho_arquivo = salvar_arquivo(arquivo, documento.id, professor_id)
    print(f'ARQUIVO SALVO NO DIRETÓRIO DO PROFESSOR COM SUCESSO!')
    
    # 3. Extrai o texto em Markdown usando Docling
    # Usa o caminho retornado na etapa anterior
    print(f'\n(3/4). Extraindo o conteúdo do arquivo recebido')
    if nome_arquivo.endswith(('.pdf', '.docx', '.pptx', '.xlsx', '.csv', '.html', '.xhtml', '.txt', '.md', '.markdown')):
        print(f'Biblioteca a ser utilizada: Docling')
        texto_extraido = extrair_texto_markdown(caminho_arquivo)
    elif nome_arquivo.endswith('.mp4'):
        print(f'Biblioteca a ser utilizada: Whisper')
        texto_extraido = processar_video(caminho_arquivo)
    
    print(f'TEXTO EXTRAÍDO COM SUCESSO!')
    
    # 4. Salva o documento no ChromaDB
    print(f'\n(4/4). Salvando dados do documento no ChromaDB')
    salvar_documento_vetor(documento.id, documento.titulo, professor_id, materia_ids, documento.timestamp, texto_extraido)
    print(f'DOCUMENTO SALVO NO CHROMADB COM SUCESSO!')
    
    return {"documento_id": documento.id, "titulo": nome_arquivo}
