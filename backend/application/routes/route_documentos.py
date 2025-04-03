from flask import Blueprint, request, jsonify
from application.services.service_documento import *

documentos_bp = Blueprint('documentos', __name__)

@documentos_bp.route('/upload', methods=['POST'])
def upload_documento():
    """
    Endpoint para upload de documentos que serão processados.
    
    Espera um ou mais documentos na chave 'documentos', e parâmetros 'professor_id' e 'materia_ids'.
    """

    if 'arquivos' not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado"}), 400

    arquivos = request.files.getlist('arquivos')

    professor_id = request.form.get('professor_id')
    materia_ids = request.form.get('materia_ids')

    if not professor_id or not materia_ids:
        return jsonify({"error": "Parâmetros 'professor_id' e 'materia_ids' são obrigatórios"}), 400

    formatted_materia_ids = [uuid.UUID(materia_id) for materia_id in materia_ids.split(',')]
    
    resultados = []
    for arquivo in arquivos:
        resultado = processar_documento(arquivo, professor_id, formatted_materia_ids)
        resultados.append(resultado)
    
    return jsonify({"message": "Upload e processamento de documentos concluído.", "resultados": resultados}), 201
