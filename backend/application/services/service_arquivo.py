import os
import uuid
from datetime import datetime
from application.config import db, chroma_client
from application.models import Arquivo
from application.libs import *

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DOCUMENTOS_DIR = os.path.join(BASE_DIR, "data/documentos")

def salvar_metadados_arquivo(titulo: str, professor_id: uuid.UUID) -> Arquivo:
    """
    Salva metadados do arquivo no PostgreSQL.

    Espera receber:
    - `titulo`: str - o nome do arquivo
    - `professor_id`: uuid.UUID - o ID do professor

    Retorna a estrutura completa do arquivo gerado para uso posterior.
    """
    novo_arquivo = Arquivo(
        titulo=titulo,
        professor_id=professor_id
    )
    db.session.add(novo_arquivo)
    db.session.commit()
    return novo_arquivo

def salvar_arquivo(arquivo, documento_id: uuid.UUID, professor_id: uuid.UUID) -> str:
    """
    Salva o arquivo recebido no diretório do professor e retorna seu caminho.

    Espera receber:
    - `arquivo`: File - o arquivo a ser salvo
    - `documento_id`: uuid.UUID - o ID do documento
    - `professor_id`: uuid.UUID - o ID do professor

    Retorna o caminho do arquivo salvo.
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

def salvar_documento_vetor(documento_id: uuid.UUID, titulo: str, professor_id: uuid.UUID, vinculos: list[dict[str, uuid.UUID]], data_upload: datetime, texto: str) -> None:
    """
    Salva dados do arquivo no ChromaDB.

    Espera receber:
    - `documento_id`: uuid.UUID - o ID do documento (gerado na 1ª etapa do processamento)
    - `titulo`: str - o nome do arquivo
    - `professor_id`: uuid.UUID - o ID do professor
    - `vinculos`: str - os vínculos entre turmas e matérias, no formato 'turma1-materia1,turma2-materia1,turma3materia2'
    - `data_upload`: datetime - a data de upload
    - `texto`: str - o texto extraído do arquivo
    """
    collection = chroma_client.get_or_create_collection("documentos")
    collection.add(
        ids=[str(documento_id)],
        metadatas=[{
            "titulo": titulo,
            "professor_id": str(professor_id),
            "vinculos": vinculos,
            "tipo": "pdf",
            "data_upload": data_upload.isoformat(),
        }],
        documents=[texto]
    )

def processar_arquivo(arquivo, professor_id: uuid.UUID, vinculos: list[dict[str, uuid.UUID]]) -> dict:
    """
    Processa um arquivo.

    Espera receber:
    - `arquivo`: File - o arquivo a ser processado
    - `professor_id`: uuid.UUID - o ID do professor
    - `vinculos`: list[dict[str, uuid.UUID]] - os vínculos entre turmas e matérias

    1. Salva metadados no PostgreSQL
    2. Salva o arquivo recebido no diretório do professor
    3. Extrai o conteúdo do arquivo utilizando a biblioteca correta de acordo com a sua extensão (PDF, DOCX, MP4, etc)
    4. Indexa no ChromaDB utilizando o mesmo ID do PostgreSQL

    Retorna um dicionário com informações do documento.
    """
    print(f'\n\nIniciando processamento do arquivo: {arquivo.filename}')

    # 1. Salva metadados no PostgreSQL e retorna a estrutura completa do documento
    print(f'\n(1/4). Salvando metadados do arquivo no PostgreSQL')
    nome_arquivo = arquivo.filename
    documento = salvar_metadados_arquivo(nome_arquivo, professor_id)
    print(f'DADOS SALVOS NO POSTGRESQL COM SUCESSO!')

    # 2. Salva o arquivo no diretório do professor e retorna o caminho para ele
    # Usa o ID retornado na etapa anterior
    print(f'\n(2/4). Salvando arquivo no diretório do professor')
    caminho_arquivo = salvar_arquivo(arquivo, documento.id, professor_id)
    print(f'ARQUIVO SALVO NO DIRETÓRIO DO PROFESSOR COM SUCESSO!')
    
    # 3. Extrai o texto do arquivo recebido
    # Usa o caminho retornado na etapa anterior
    print(f'\n(3/4). Extraindo o conteúdo do arquivo recebido')
    try:
        if nome_arquivo.endswith(('.pdf', '.docx', '.pptx', '.xlsx', '.csv', '.html', '.xhtml', '.txt', '.md', '.markdown')):
            print(f'Biblioteca a ser utilizada: Docling')
            texto_extraido = extrair_texto_markdown(caminho_arquivo) # Extrai o texto em Markdown usando Docling
        elif nome_arquivo.endswith(('.mp4', '.mov', '.mkv', '.avi', '.mp3', '.wav', '.m4a', '.flac', '.ogg')):
            print(f'Biblioteca a ser utilizada: Whisper')
            texto_extraido = processar_video(caminho_arquivo) # Extrai o texto do vídeo/áudio usando Whisper e FFmpeg
        else:
            print(f'Tipo de arquivo não suportado: {nome_arquivo}')
            return {
                "filename": nome_arquivo,
                "status": 400,
                "message": "Tipo de arquivo não suportado"
            }
    except Exception as e:
        print(f"Erro ao extrair o conteúdo do arquivo: {str(e)}")
        return {
            "filename": nome_arquivo,
            "status": 500,
            "message": "Erro ao extrair o conteúdo do arquivo"
        }
    
    if texto_extraido is not None:
        print(f'TEXTO EXTRAÍDO COM SUCESSO!')
    
    # 4. Salva o documento no ChromaDB
    print(f'\n(4/4). Salvando dados do documento no ChromaDB')

    # Junta todas as relações em uma string, separando-as por vírgulas. Cada relação possui um UUID de turma e um UUID de matéria, separados por hífen
    formatted_vinculos = ','.join([f'{v["turma_id"]}-{v["materia_id"]}' for v in vinculos]) # Exemplo: 'turma1-materia1,turma2-materia1,turma3materia2'
    salvar_documento_vetor(documento.id, documento.titulo, professor_id, formatted_vinculos, documento.data_upload, texto_extraido)
    print(f'DOCUMENTO SALVO NO CHROMADB COM SUCESSO!')
    
    return {
        "filename": nome_arquivo,
        "status": 201,
        "message": "Arquivo processado com sucesso",
        "data": {
            "documento_id": documento.id,
            "titulo": documento.titulo,
            "data_upload": documento.data_upload
        }
    }
