"""
Rotas para lidar com arquivos.
"""

from flask import Blueprint, request, jsonify
import json
from application.services.service_arquivo import *
from application.services.service_professor import *
from application.services.service_turma import *
from application.services.service_materia import *

arquivos_bp = Blueprint('arquivos', __name__)

@arquivos_bp.route('/upload', methods=['POST'])
def upload_arquivos():
    """
    Endpoint para upload de arquivos que serão processados.

    Espera receber:
    - `arquivos`: list - um ou mais arquivos
    - `matricula_professor`: str - o número de matrícula do professor
    - `vinculos`: str - um ou mais códigos de turma e matéria, separados por vírgula
    """
    print(f'\n\nRequisição recebida!')
    print(request.files)

    if 'arquivos' not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado"}), 400

    # Verifica se os dados necessários estão presentes
    arquivos = request.files.getlist('arquivos')
    matricula_professor = request.form.get('matricula_professor')
    vinculos_raw = request.form.get('vinculos') # Mesmo recebendo numa estrutura JSON, ele virá como string

    if not matricula_professor or not vinculos_raw:
        return jsonify({"error": "Parâmetros 'matricula_professor' e 'vinculos' são obrigatórios"}), 400
    print(f'\n\nNomes dos arquivos recebidos: {[arquivo.filename for arquivo in arquivos]}\r\nMatrícula de professor recebida: {matricula_professor}\r\nVínculos recebidos:\n{vinculos_raw}')

    # Deserializa os dados de vínculos
    try:
        vinculos = json.loads(vinculos_raw)
        if not isinstance(vinculos, list):
            raise ValueError
    except ValueError:
        return jsonify({"error": "Parâmetro 'vinculos' deve ser um JSON válido"}), 400
    
    # Valida o professor
    professor_id = buscar_id_professor_por_matricula(matricula_professor)
    if not professor_id:
        print(f"Professor com matrícula '{matricula_professor}' não encontrado")
        return jsonify({"error": f"Professor com matrícula '{matricula_professor}' não encontrado"}), 404
    
    # Valida os vínculos
    vinculos_processados: list[dict[str, uuid.UUID]] = []
    for vinculo in vinculos:
        codigo_turma = vinculo.get('codigo_turma')
        codigo_materia = vinculo.get('codigo_materia')

        if not codigo_turma or not codigo_materia:
            return jsonify({"error": "Cada vínculo deve conter 'codigo_turma' e 'codigo_materia'"}), 400
        
        # Busca o UUID da turma
        turma_id = buscar_id_turma_por_codigo(codigo_turma)
        if not turma_id:
            print(f"Código de turma '{codigo_turma}' não encontrado")
            return jsonify({"error": f"Código de turma '{codigo_turma}' não encontrado"}), 404
        
        # Busca o UUID da matéria
        materia_id = buscar_id_materia_por_codigo(codigo_materia)
        if not materia_id:
            print(f"Código de matéria '{codigo_materia}' não encontrado")
            return jsonify({"error": f"Código de matéria '{codigo_materia}' não encontrado"}), 404
        
        # Adiciona o vínculo processado
        vinculos_processados.append({"turma_id": turma_id, "materia_id": materia_id})
    
    resultados = []
    for arquivo in arquivos:
        print(f'\n\nEnviando arquivo para iniciar o processamento: {arquivo.filename}')
        resultado = processar_arquivo(arquivo, professor_id, vinculos_processados)
        resultados.append(resultado)
    
    return jsonify({"message": "Upload e processamento de documentos concluído.", "resultados": resultados}), 201
