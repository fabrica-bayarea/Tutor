import os
import uuid
import glob
from datetime import datetime
from application.config.database import db
from application.config.vector_database import collection
from application.models import Arquivo
from application.libs.docling_handler import extrair_texto_markdown
from application.libs.scraping_handler import data_extraction
from application.libs.whisper_handler import processar_video
from application.services.service_vinculos import criar_vinculo_arquivo_turma_materia

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DOCUMENTOS_DIR = os.path.join(BASE_DIR, "data/documentos")

EXTENSOES_SUPORTADAS = {
    "texto": (".pdf", ".docx", ".pptx", ".xlsx", ".csv", ".html", ".xhtml", ".md", ".markdown"),
    "video-audio": (".mp4", ".mov", ".mkv", ".avi", ".mp3", ".wav", ".m4a", ".flac", ".ogg")
}

CARACTERES_NAO_PERMITIDOS = '|<>:"/\\?*'

def salvar_metadados_arquivo(titulo: str, professor_id: uuid.UUID) -> Arquivo:
    """
    Função atômica, responsável por salvar metadados do arquivo no PostgreSQL.

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
    Função atômica, responsável por salvar o arquivo recebido no diretório do professor e retornar seu caminho.

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

def salvar_documento_vetor(documento_id: uuid.UUID, titulo: str, professor_id: uuid.UUID, formatted_vinculos: str, data_upload: datetime, texto: str) -> None:
    """
    Função atômica, responsável por salvar dados do arquivo no ChromaDB.

    Espera receber:
    - `documento_id`: uuid.UUID - o ID do documento (gerado na 1ª etapa do processamento)
    - `titulo`: str - o nome do arquivo
    - `professor_id`: uuid.UUID - o ID do professor
    - `vinculos`: str - os vínculos entre turmas e matérias, no formato 'turma1_materia1,turma2_materia1,turma3_materia2'
    - `data_upload`: datetime - a data de upload
    - `texto`: str - o texto extraído do arquivo
    """
    collection.add(
        ids=[str(documento_id)],
        metadatas=[{
            "titulo": titulo,
            "professor_id": str(professor_id),
            "vinculos": formatted_vinculos,
            "tipo": "pdf",
            "data_upload": data_upload.isoformat(),
        }],
        documents=[texto]
    )

def processar_arquivo(arquivo, professor_id: uuid.UUID, vinculos: list[dict[str, uuid.UUID]]) -> dict:
    """
    Função principal, responsável por processar um arquivo.

    Espera receber:
    - `arquivo`: File - o arquivo a ser processado
    - `professor_id`: uuid.UUID - o ID do professor
    - `vinculos`: list[dict[str, uuid.UUID]] - os vínculos entre turmas e matérias

    1. Salva metadados no PostgreSQL
        1.1. Cria um novo registro de Arquivo
        1.2. Cria um novo registro de ArquivoTurmaMateria para cada vínculo recebido
    2. Salva o arquivo recebido no diretório do professor
    3. Extrai o conteúdo do arquivo utilizando a biblioteca correta de acordo com a sua extensão (PDF, DOCX, MP4, etc)
    4. Indexa no ChromaDB utilizando o mesmo ID do PostgreSQL

    Retorna um dicionário com informações do documento.
    """
    print(f'\n\nIniciando processamento do arquivo: {arquivo.filename}')

    # Verifica se o arquivo é suportado
    nome_arquivo = arquivo.filename
    extensao_arquivo = str(os.path.splitext(nome_arquivo)[1])

    if not any(extensao_arquivo in extensao for extensao in EXTENSOES_SUPORTADAS.values()):
        print(f'Não é possível processar o arquivo {nome_arquivo} devido à sua extensão ({extensao_arquivo})')
        return {
            "filename": nome_arquivo,
            "status": 400,
            "message": "Tipo de arquivo não suportado"
        }

    # 1. Salva metadados no PostgreSQL
    print(f'\n(1/4). Salvando metadados no PostgreSQL')
    # 1.1. Salva os metadados do arquivo no PostgreSQL e retorna a estrutura completa do documento
    print(f'\n(1.1/4). Salvando metadados do Arquivo no PostgreSQL')
    documento = salvar_metadados_arquivo(nome_arquivo, professor_id)
    print(f'ARQUIVO SALVO NO POSTGRESQL COM SUCESSO!')

    # 1.2. Salva os vínculos no PostgreSQL
    print(f'\n(1.2/4). Salvando vínculos ArquivoTurmaMateria no PostgreSQL')
    vinculos_arquivo_turma_materia = []
    for vinculo in vinculos:
        vinculo_arquivo_turma_materia = criar_vinculo_arquivo_turma_materia(documento.id, vinculo['turma_id'], vinculo['materia_id'])
        vinculos_arquivo_turma_materia.append(vinculo_arquivo_turma_materia)
        print(f'Vínculo salvo: {vinculo_arquivo_turma_materia}')
    
    print(f'VÍNCULOS ARQUIVO-TURMA-MATERIA SALVOS NO POSTGRESQL COM SUCESSO!')

    # 2. Salva o arquivo no diretório do professor e retorna o caminho para ele
    # Usa o ID retornado na etapa anterior
    print(f'\n(2/4). Salvando arquivo no diretório do professor')
    caminho_arquivo = salvar_arquivo(arquivo, documento.id, professor_id)
    print(f'ARQUIVO SALVO NO DIRETÓRIO DO PROFESSOR COM SUCESSO!')
    
    # 3. Extrai o texto do arquivo recebido
    # Usa o caminho retornado na etapa anterior
    print(f'\n(3/4). Extraindo o conteúdo do arquivo recebido')
    try:
        if extensao_arquivo in EXTENSOES_SUPORTADAS['texto']:
            print(f'Biblioteca a ser utilizada: Docling')
            texto_extraido = extrair_texto_markdown(caminho_arquivo) # Extrai o texto em Markdown usando Docling
        elif extensao_arquivo in EXTENSOES_SUPORTADAS['video-audio']:
            print(f'Biblioteca a ser utilizada: Whisper')
            texto_extraido = processar_video(caminho_arquivo) # Extrai o texto do vídeo/áudio usando Whisper e FFmpeg
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

    # Junta todas as relações em uma string, separando-as por vírgulas. Cada relação possui um UUID de turma e um UUID de matéria, separados por underscore
    formatted_vinculos = ','.join([f'{v["turma_id"]}_{v["materia_id"]}' for v in vinculos]) # Exemplo: 'turma1_materia1,turma2_materia1,turma3_materia2'
    salvar_documento_vetor(documento.id, documento.titulo, professor_id, formatted_vinculos, documento.data_upload, texto_extraido)
    print(f'DOCUMENTO SALVO NO CHROMADB COM SUCESSO!')
    
    return {
        "filename": nome_arquivo,
        "status": 201,
        "message": "Arquivo processado com sucesso",
        "data": {
            "documento_id": documento.id,
            "professor_id": professor_id,
            "titulo": documento.titulo,
            "data_upload": documento.data_upload
        }
    }

def processar_link(link: str, driver, professor_id: uuid.UUID, vinculos: list[dict[str, uuid.UUID]]) -> dict:
    """
    Função principal, responsável por processar um link.

    Espera receber:
    - `link`: str - o link a ser processado
    - `driver`: webdriver - o driver do navegador
    - `professor_id`: uuid.UUID - o ID do professor
    - `vinculos`: list[dict[str, uuid.UUID]] - os vínculos entre turmas e matérias

    1. Extrai o conteúdo do link recebido
    2. Salva metadados no PostgreSQL
        2.1. Cria um novo registro de Arquivo
        2.2. Cria um novo registro de ArquivoTurmaMateria para cada vínculo recebido
    3. Salva o conteúdo extraído do link num arquivo `.txt` no diretório do professor
    4. Indexa no ChromaDB utilizando o mesmo ID do PostgreSQL

    Retorna um dicionário com informações do documento.
    """
    
    print(f'\nProcessando link: {link}')
    
    # 1. Extrai o conteúdo do link recebido
    print(f'\n(1/4). Extraindo o conteúdo do link recebido')
    dados_extrair_link = data_extraction(driver, link)
    
    # 2. Salva metadados no PostgreSQL        
    print(f'\n(2/4). Salvando metadados no PostgreSQL')
    print(f'\n(2.1/4). Criando um novo registro de Arquivo')
    documento = salvar_metadados_arquivo(dados_extrair_link['page_title'], professor_id)
    print(f'\n(2.2/4). Criando um novo registro de ArquivoTurmaMateria para cada vínculo recebido')
    vinculos_arquivos_turmas_materias = []
    for vinculo in vinculos:
        vinculo_arquivo_turma_materia = criar_vinculo_arquivo_turma_materia(documento.id, vinculo['turma_id'], vinculo['materia_id'])
        vinculos_arquivos_turmas_materias.append(vinculo_arquivo_turma_materia)
          
    # salvando o conteudo do link recebido no arquivo .txt
    print(f'\n(3/4). Salvando o conteúdo extraído do link num arquivo `.txt` no diretório do professor')
    nome_arquivo = f"{documento.id}_{documento.titulo.replace(' ', '_')}"
    for caractere in CARACTERES_NAO_PERMITIDOS:
        nome_arquivo = nome_arquivo.replace(caractere, '_')
    nome_arquivo += '.txt'
    caminho_arquivo = os.path.join(
        DOCUMENTOS_DIR,
        str(professor_id),
        str(nome_arquivo)
    )
    print(f'Caminho do arquivo: {caminho_arquivo}')
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(dados_extrair_link['content'])
    
    # 4. Indexa no ChromaDB utilizando o mesmo ID do PostgreSQL
    print(f'\n(4/4). Salvando dados do documento no ChromaDB')
    formatted_vinculos = ','.join([f'{v["turma_id"]}_{v["materia_id"]}' for v in vinculos]) # Exemplo: 'turma1_materia1,turma2_materia1,turma3_materia2'
    salvar_documento_vetor(documento.id, documento.titulo, professor_id, formatted_vinculos, documento.data_upload, dados_extrair_link['content'])
    
    return {
        "status": 201,
        "message": "Link processado com sucesso",
        "data": {
            "documento_id": documento.id,
            "professor_id": professor_id,
            "titulo": documento.titulo,
            "data_upload": documento.data_upload
        }
    }

def processar_texto(texto: str, professor_id: uuid.UUID, vinculos: list[dict[str, uuid.UUID]]) -> list[dict]:
    """Função responsavel por receber os textos e armazená-los no banco de dados e no sistema de arquivos.
    Espera receber:
    - `texto`: str - um texto
    - `professor_id`: uuid.UUID - o ID do professor
    - `vinculos`: list[dict[str, uuid.UUID]] - os vínculos entre turmas e matérias
    
    1. Salva metadados no PostgreSQL
        1.1. Cria um novo registro de Arquivo
        1.2. Cria um novo registro de ArquivoTurmaMateria para cada vínculo recebido
    2. Salva os textos em arquivos no formato `.txt` no diretório do professor
    3. Indexa no ChromaDB utilizando o mesmo ID do PostgreSQL
    
    Retorna uma lista de dicionários com informações do documento.
    """
    
    print(f'\nIniciando processamento do texto:')
    titulo = f"Texto_{uuid.uuid4()}" # Gera um título único para o texto
    print(f'\n(1/4). Salvando metadados no PostgreSQL para o texto: {titulo}')

    # 1. Salva metadados no PostgreSQL
    print(f'\n(1.1/4). Criando um novo registro de Arquivo')
    documento = salvar_metadados_arquivo(titulo, professor_id)

    # 1.2. Cria um novo registro de ArquivoTurmaMateria para cada vínculo recebido
    print(f'\n(1.2/4). Criando um novo registro de ArquivoTurmaMateria para cada vínculo recebido')
    vinculos_arquivo_turma_materia = []
    for vinculo in vinculos:
        vinculo_arquivo_turma_materia = criar_vinculo_arquivo_turma_materia(documento.id, vinculo['turma_id'], vinculo['materia_id'])
        vinculos_arquivo_turma_materia.append(vinculo_arquivo_turma_materia)
    
    # 2. Salva o texto em um arquivo no diretório do professor
    print(f'\n(2/4). Salvando o texto em um arquivo no diretório do professor')
    nome_arquivo = f"{documento.id}_{titulo.replace(' ', '_')}.txt"
    for caractere in CARACTERES_NAO_PERMITIDOS:
        nome_arquivo = nome_arquivo.replace(caractere, '_')
    nome_arquivo += '.txt'
    caminho_arquivo = os.path.join(
        DOCUMENTOS_DIR,
        str(professor_id),
        str(nome_arquivo)
    )
    print(f'Caminho do arquivo: {caminho_arquivo}')
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(texto)
        
    # 3. Indexa no ChromaDB utilizando o mesmo ID do PostgreSQL
    print(f'\n(3/4). Salvando dados do documento no ChromaDB')
    formatted_vinculos = ','.join([f'{v["turma_id"]}_{v["materia_id"]}' for v in vinculos])
    salvar_documento_vetor(documento.id, documento.titulo, professor_id, formatted_vinculos, documento.data_upload, texto)
    print(f'DOCUMENTO SALVO NO CHROMADB COM SUCESSO!')

    return {
        "status": 201,
        "message": "texto processado com sucesso",
        "data": {
            "documento_id": documento.id,
            "professor_id": professor_id,
            "titulo": documento.titulo,
            "data_upload": documento.data_upload
        }
    }

def obter_arquivo_real_por_id(professor_id: uuid.UUID, arquivo_id: uuid.UUID) -> tuple:
    """
    Função atômica, responsável por obter o arquivo real, salvo no sistema de arquivos, a partir do seu ID.

    Espera receber:
    - `professor_id`: uuid.UUID - o ID do professor
    - `arquivo_id`: uuid.UUID - o ID do arquivo

    Retorna um tuple com o caminho do arquivo e o arquivo em si.
    """
    caminho_arquivo = os.path.join(DOCUMENTOS_DIR, str(professor_id), f"{arquivo_id}_*")
    arquivos_encontrados = glob.glob(caminho_arquivo)

    if len(arquivos_encontrados) == 0:
        raise ValueError(f"Arquivo {arquivo_id} não encontrado")

    caminho_arquivo = arquivos_encontrados[0]
    extensao_arquivo = os.path.splitext(caminho_arquivo)[1]

    with open(caminho_arquivo, 'rb') as f:
        conteudo_arquivo = f.read()
    
    return caminho_arquivo, conteudo_arquivo, extensao_arquivo

def obter_arquivos_turma_materia(turma_id: uuid.UUID, materia_id: uuid.UUID) -> list[Arquivo]:
    """
    Função atômica, responsável por obter todos os arquivos de uma turma associada a uma matéria no PostgreSQL.

    Espera receber:
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna uma lista de arquivos.
    """
    arquivos = Arquivo.query.filter_by(turma_id=turma_id, materia_id=materia_id).all()
    return [arquivo.to_dict() for arquivo in arquivos]
