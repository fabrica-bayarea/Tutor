"""
Rotas para lidar com arquivos.
"""

from flask import Blueprint, request, jsonify
from application.services.service_arquivo import *

arquivos_bp = Blueprint('arquivos', __name__)

@arquivos_bp.route('/upload', methods=['POST'])
def upload_arquivos():
    """
    Endpoint para upload de arquivos que serão processados.
    
    Espera um ou mais arquivos na chave 'arquivos', e parâmetros 'professor_id' e 'materia_ids'.
    """
    print(f'\n\nRequisição recebida!')
    print(request.files)

    if 'arquivos' not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado"}), 400

    arquivos = request.files.getlist('arquivos')

    professor_id = request.form.get('professor_id')
    turma_ids = request.form.get('turma_ids')
    materia_ids = request.form.get('materia_ids')

    if not professor_id or not turma_ids or not materia_ids:
        return jsonify({"error": "Parâmetros 'professor_id', 'turma_ids' e 'materia_ids' são obrigatórios"}), 400
    print(f'\n\nNomes dos arquivos recebidos: {[arquivo.filename for arquivo in arquivos]}\nID de professor recebido: {professor_id}\nIDs de matérias recebidos: {materia_ids}')

    formatted_materia_ids = [uuid.UUID(materia_id) for materia_id in materia_ids.split(',')]
    print(f'\n\nIDs de matérias formatados: {formatted_materia_ids}')

    resultados = []
    for arquivo in arquivos:
        print(f'\n\nEnviando arquivo para iniciar o processamento: {arquivo.filename}')
        resultado = processar_arquivo(arquivo, professor_id, formatted_materia_ids)
        resultados.append(resultado)
    
    return jsonify({"message": "Upload e processamento de documentos concluído.", "resultados": resultados}), 201
