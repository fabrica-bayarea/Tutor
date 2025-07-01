"""
Rotas para lidar com arquivos.
"""
from flask import Blueprint, request, jsonify, g, send_file
import uuid
import json
import time
import os
from application.auth.auth_decorators import token_obrigatorio, apenas_professores
from application.services.service_arquivo import processar_arquivo, processar_link, obter_arquivo_real_por_id, obter_arquivos_turma_materia
from application.libs.scraping_handler import configure_browser
from urllib.parse import urlparse
from application.utils.validacoes import validar_professor_turma_materia

arquivos_bp = Blueprint('arquivos', __name__)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

@arquivos_bp.route('/upload/arquivos', methods=['POST'])
@token_obrigatorio
@apenas_professores
def upload_arquivos():
    """
    Endpoint para upload de arquivos que serão processados.

    Espera receber:
    - `arquivos`: list - um ou mais arquivos
    - `vinculos`: list[dict[str, uuid.UUID]] - um ou mais vínculos entre turmas e matérias

    1. Verifica se os dados necessários estão presentes
    2. Verifica se os vínculos enviados são válidos
    3. Verifica se os arquivos enviados são válidos
    4. Processa cada arquivo
    
    Retorna os resultados do processamento de arquivos.
    """
    print(f'\n\nRequisição recebida!')
    print(request.files)

    # Verifica se os dados necessários estão presentes
    arquivos = request.files.getlist('arquivos')
    vinculos_raw = request.form.get('vinculos')

    if not arquivos or all(arquivo.filename == '' for arquivo in arquivos):
        return jsonify({"error": "Nenhum arquivo foi enviado"}), 400

    if not vinculos_raw:
        return jsonify({"error": "Parâmetro 'vinculos' é obrigatório"}), 400

    print(f'\n\nNomes dos arquivos recebidos: {[arquivo.filename for arquivo in arquivos]}\nVínculos recebidos:\n{vinculos_raw}')

    try:
        vinculos = json.loads(vinculos_raw)
        if not isinstance(vinculos, list):
            raise ValueError
    except ValueError:
        return jsonify({"error": "Parâmetro 'vinculos' deve ser um JSON válido"}), 400
    
    # Deserializa os vínculos
    vinculos_processados: list[dict[str, uuid.UUID]] = []
    for vinculo in vinculos:
        try:
            turma_id = uuid.UUID(vinculo.get('turma_id'))
            materia_id = uuid.UUID(vinculo.get('materia_id'))
        except (ValueError, TypeError):
            return jsonify({"error": "IDs de turma e matéria devem ser UUIDs válidos"}), 400

        if not turma_id or not materia_id:
            return jsonify({"error": "Cada vínculo deve conter 'turma_id' e 'materia_id'"}), 400
        
        # Valida a existência do vínculo entre o professor, a turma e a matéria
        vinculo_existe = validar_professor_turma_materia(g.usuario_id, turma_id, materia_id)
        if not vinculo_existe:
            print(f"Vínculo entre professor '{g.usuario_id}', turma '{turma_id}' e matéria '{materia_id}' não encontrado")
            return jsonify({"error": f"Vínculo não encontrado para turma '{turma_id}' e matéria '{materia_id}'"}), 404

        # Adiciona o vínculo à lista de vínculos processados
        vinculos_processados.append({"turma_id": turma_id, "materia_id": materia_id})

    # Processa cada arquivo
    resultados = []
    for arquivo in arquivos:
        print(f'\n\nEnviando arquivo para iniciar o processamento: {arquivo.filename}')
        resultado = processar_arquivo(arquivo, g.usuario_id, vinculos_processados)
        resultados.append(resultado)

    if all(r.get('status') == 201 for r in resultados):
        return jsonify({"message": "Todos os arquivos foram processados com sucesso", "results": resultados}), 201
    elif all(r.get('status') in [400, 500] for r in resultados):
        return jsonify({"message": "Erro ao processar todos os arquivos", "results": resultados}), resultados[0].get('status')
    else:
        return jsonify({"message": "Alguns arquivos foram processados com sucesso, mas outros falharam", "results": resultados}), 207

@arquivos_bp.route('/upload/links', methods=['POST'])
@token_obrigatorio
@apenas_professores
def upload_links():
    """
    Endpoint para upload de arquivos que serão processados.

    Espera receber:
    - `links`: list[str] - uma lista com um ou mais links
    - `vinculos`: list[dict[str, uuid.UUID]] - uma lista com um ou mais vínculos entre turmas e matérias

    1. Verifica se os dados necessários estão presentes
    2. Verifica se os vínculos enviados são válidos
    3. Processa cada link
    
    Retorna os resultados do processamento de links.
    """
    # Verifica se os dados necessários estão presentes
    urls = request.json.get('urls')
    vinculos = request.json.get('vinculos')

    if not urls or not vinculos:
        return jsonify({"error": "Parâmetros 'urls' e 'vinculos' são obrigatórios"}), 400
    
    # Verifica se os links são válidos
    urls_invalidos = []
    for url in urls:
        if not is_valid_url(url):
            urls_invalidos.append(url)
    
    if urls_invalidos:
        return jsonify({"error": f"URLs inválidas: {urls_invalidos}"}), 400
    
    # Deserializa os vínculos
    vinculos_processados: list[dict[str, uuid.UUID]] = []
    for vinculo in vinculos:
        try:
            turma_id = uuid.UUID(vinculo.get('turma_id'))
            materia_id = uuid.UUID(vinculo.get('materia_id'))
        except (ValueError, TypeError):
            return jsonify({"error": "IDs de turma e matéria devem ser UUIDs válidos"}), 400

        if not turma_id or not materia_id:
            return jsonify({"error": "Cada vínculo deve conter 'turma_id' e 'materia_id'"}), 400
        
        # Valida a existência do vínculo entre o professor, a turma e a matéria
        vinculo_existe = validar_professor_turma_materia(g.usuario_id, turma_id, materia_id)
        if not vinculo_existe:
            print(f"Vínculo entre professor '{g.usuario_id}', turma '{turma_id}' e matéria '{materia_id}' não encontrado")
            return jsonify({"error": f"Vínculo não encontrado para turma '{turma_id}' e matéria '{materia_id}'"}), 404

        # Adiciona o vínculo à lista de vínculos processados
        vinculos_processados.append({"turma_id": turma_id, "materia_id": materia_id})
    
    # Configura o driver do navegador para realizar o scraping
    driver = configure_browser()

    # Processa cada link
    resultados = []
    for url in urls:
        resultado = processar_link(url, driver, g.usuario_id, vinculos_processados)
        resultados.append(resultado)
        #time.sleep(2)
    
    driver.quit()
    
    if all(r.get('status') == 201 for r in resultados):
        return jsonify({"message": "Todos os links foram processados com sucesso", "results": resultados}), 201
    elif all(r.get('status') in [400, 500] for r in resultados):
        return jsonify({"message": "Erro ao processar todos os links", "results": resultados}), resultados[0].get('status')
    else:
        return jsonify({"message": "Alguns links foram processados com sucesso, mas outros falharam", "results": resultados}), 207

@arquivos_bp.route('/<string:turma_id>_<string:materia_id>', methods=['GET'])
@token_obrigatorio
def obter_arquivos_por_turma_materia(turma_id: uuid.UUID, materia_id: uuid.UUID):
    """
    Endpoint para obter TODOS os arquivos de uma matéria associada a uma turma.

    Apenas professores com vínculo podem acessar.

    Espera receber:
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    1. Valida o professor
    2. Busca os arquivos associados à turma e matéria
    
    Retorna os arquivos encontrados.
    """
    # Valida se o professor tem vínculo com a turma e matéria
    if not validar_professor_turma_materia(g.usuario_id, turma_id, materia_id):
        return jsonify({"error": "Acesso não autorizado para esta turma/matéria"}), 403

    # Busca os arquivos associados à turma e matéria
    try:
        arquivos = obter_arquivos_turma_materia(turma_id, materia_id)
    except ValueError as e:
        print(f'Erro ao buscar arquivos: {str(e)}')
        return jsonify({"error": str(e)}), 400

    # Retorna os arquivos encontrados
    return jsonify(arquivos), 200

@arquivos_bp.route('/download/<string:arquivo_id>', methods=['GET'])
@token_obrigatorio
@apenas_professores
def download_arquivo(arquivo_id: str):
    """
    Endpoint para baixar/visualizar um arquivo pelo seu ID.

    Espera receber:
    - `arquivo_id`: str - o ID do arquivo a ser baixado

    Retorna o arquivo para download/visualização no navegador.
    """
    try:
        # Converte a string do ID para UUID
        arquivo_uuid = uuid.UUID(arquivo_id)
        
        # Obtém o arquivo real do sistema de arquivos
        caminho_arquivo, conteudo_arquivo, extensao = obter_arquivo_real_por_id(g.usuario_id, arquivo_uuid)
        
        # Obtém o nome do arquivo original (sem o ID e sem o caminho)
        nome_arquivo = os.path.basename(caminho_arquivo)
        # Remove o UUID do início do nome do arquivo (formato: UUID_nome_original.extensao)
        nome_original = '_'.join(nome_arquivo.split('_')[1:]) if '_' in nome_arquivo else nome_arquivo
        
        # Cria um arquivo temporário em memória para enviar como resposta
        from io import BytesIO
        file_obj = BytesIO(conteudo_arquivo)
        
        # Determina o mimetype com base na extensão do arquivo
        import mimetypes
        mimetype = mimetypes.guess_type(nome_original)[0] or 'application/octet-stream'
        
        # Se for um tipo de arquivo que pode ser visualizado no navegador, use inline
        # Caso contrário, force o download
        as_attachment = mimetype not in [
            'application/pdf',
            'image/jpeg', 'image/png', 'image/gif',
            'text/plain', 'text/html',
            'application/json'
        ]
        
        return send_file(
            file_obj,
            mimetype=mimetype,
            as_attachment=as_attachment,
            download_name=nome_original
        )
        
    except ValueError as e:
        # Se o UUID for inválido ou o arquivo não for encontrado
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        # Para outros erros inesperados
        print(f"Erro ao baixar o arquivo: {str(e)}")
        return jsonify({"error": "Erro ao processar o arquivo"}), 500
