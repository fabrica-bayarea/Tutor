"""
Rotas para lidar com arquivos.
"""

from flask import Blueprint, request, jsonify
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
    - `codigos_turma`: str - um ou mais códigos de turma, separados por vírgula
    - `codigos_materia`: str - um ou mais códigos de matéria, separados por vírgula
    """
    print(f'\n\nRequisição recebida!')
    print(request.files)

    if 'arquivos' not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado"}), 400

    # Verifica se os dados necessários estão presentes
    arquivos = request.files.getlist('arquivos')
    matricula_professor = request.form.get('matricula_professor')
    codigos_turma = request.form.get('codigos_turma')
    codigos_materia = request.form.get('codigos_materia')

    if not matricula_professor or not codigos_turma or not codigos_materia:
        return jsonify({"error": "Parâmetros 'matricula_professor', 'codigos_turma' e 'codigos_materia' são obrigatórios"}), 400
    print(f'\n\nNomes dos arquivos recebidos: {[arquivo.filename for arquivo in arquivos]}\r\nMatrícula de professor recebida: {matricula_professor}\r\nCódigos de turma recebidos: {codigos_turma}\r\nCódigos de matéria recebidos: {codigos_materia}')

    formatted_codigos_turma = [codigo_turma for codigo_turma in codigos_turma.split(',')]
    formatted_codigos_materia = [codigo_materia for codigo_materia in codigos_materia.split(',')]
    print(f'\n\nCódigos de turma formatados: {formatted_codigos_turma}\r\nCódigos de matéria formatados: {formatted_codigos_materia}')

    # Valida dados enviados
    professor_id = buscar_id_professor_por_matricula(matricula_professor)
    if not professor_id:
        print(f"Professor com matrícula '{matricula_professor}' não encontrado")
        return jsonify({"error": f"Professor com matrícula '{matricula_professor}' não encontrado"}), 404
    
    formatted_turma_ids = []
    for codigo_turma in formatted_codigos_turma:
        turma_id = buscar_id_turma_por_codigo(codigo_turma)
        if not turma_id:
            print(f"Código de turma '{codigo_turma}' não encontrado")
            return jsonify({"error": f"Código de turma '{codigo_turma}' não encontrado"}), 404
        
        formatted_turma_ids.append(turma_id)
    
    formatted_materia_ids = []
    for codigo_materia in formatted_codigos_materia:
        materia_id = buscar_id_materia_por_codigo(codigo_materia)
        if not materia_id:
            print(f"Código de matéria '{codigo_materia}' não encontrado")
            return jsonify({"error": f"Código de matéria '{codigo_materia}' não encontrado"}), 404
        
        formatted_materia_ids.append(materia_id)
    
    resultados = []
    for arquivo in arquivos:
        print(f'\n\nEnviando arquivo para iniciar o processamento: {arquivo.filename}')
        resultado = processar_arquivo(arquivo, professor_id, formatted_turma_ids, formatted_materia_ids)
        resultados.append(resultado)
    
    return jsonify({"message": "Upload e processamento de documentos concluído.", "resultados": resultados}), 201
