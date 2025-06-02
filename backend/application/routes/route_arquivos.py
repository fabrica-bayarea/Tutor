"""
Rotas para lidar com arquivos.
"""
from flask import Blueprint, request, jsonify
import uuid
import json
from application.services.service_arquivo import *
from application.services.service_professor import *
from application.services.service_turma import *
from application.services.service_materia import *
from application.utils.validacoes import validar_professor, validar_turma, validar_materia, validar_professor_turma_materia

arquivos_bp = Blueprint('arquivos', __name__)

@arquivos_bp.route('/upload', methods=['POST'])
def upload_arquivos():
    """
    Endpoint para upload de arquivos que serão processados.

    Espera receber:
    - `arquivos`: list - um ou mais arquivos
    - `professor_id`: uuid.UUID - o ID do professor
    - `vinculos`: list[dict[str, uuid.UUID]] - um ou mais vínculos entre turmas e matérias
    """
    print(f'\n\nRequisição recebida!')
    print(request.files)

    # Verifica se os dados necessários estão presentes
    arquivos = request.files.getlist('arquivos')
    professor_id = uuid.UUID(request.form.get('professor_id'))
    vinculos_raw = request.form.get('vinculos') # Mesmo recebendo numa estrutura JSON, ele virá como string

    if not arquivos or all(arquivo.filename == '' for arquivo in arquivos):
        return jsonify({"error": "Nenhum arquivo foi enviado"}), 400

    if not professor_id or not vinculos_raw:
        return jsonify({"error": "Parâmetros 'professor_id' e 'vinculos' são obrigatórios"}), 400
    print(f'\n\nNomes dos arquivos recebidos: {[arquivo.filename for arquivo in arquivos]}\nID do professor recebido: {professor_id}\nVínculos recebidos:\n{vinculos_raw}')

    # Deserializa os dados de vínculos
    try:
        vinculos = json.loads(vinculos_raw)
        if not isinstance(vinculos, list):
            raise ValueError
    except ValueError:
        return jsonify({"error": "Parâmetro 'vinculos' deve ser um JSON válido"}), 400
    
    # Valida o professor
    professor_existe = validar_professor(professor_id)
    if not professor_existe:
        print(f"Professor com ID '{professor_id}' não encontrado")
        return jsonify({"error": f"Professor com ID '{professor_id}' não encontrado"}), 404

    # Valida os vínculos
    vinculos_processados: list[dict[str, uuid.UUID]] = []
    for vinculo in vinculos:
        turma_id = uuid.UUID(vinculo.get('turma_id'))
        materia_id = uuid.UUID(vinculo.get('materia_id'))

        if not turma_id or not materia_id:
            return jsonify({"error": "Cada vínculo deve conter 'turma_id' e 'materia_id'"}), 400
        
        # Valida a existência da turma
        turma_existe = validar_turma(turma_id)
        if not turma_existe:
            print(f"Turma com ID '{turma_id}' não encontrada")
            return jsonify({"error": f"Turma com ID '{turma_id}' não encontrada"}), 404

        # Valida a existência da matéria
        materia_existe = validar_materia(materia_id)
        if not materia_existe:
            print(f"Matéria com ID '{materia_id}' não encontrada")
            return jsonify({"error": f"Matéria com ID '{materia_id}' não encontrada"}), 404
        
        # Valida a existência do vínculo entre o professor, a turma e a matéria
        vinculo_existe = validar_professor_turma_materia(professor_id, turma_id, materia_id)
        if not vinculo_existe:
            print(f"Vínculo entre professor '{professor_id}', turma '{turma_id}' e matéria '{materia_id}' não encontrado")
            return jsonify({"error": f"Vínculo entre professor '{professor_id}', turma '{turma_id}' e matéria '{materia_id}' não encontrado"}), 404
        
        # Adiciona o vínculo processado
        vinculos_processados.append({"turma_id": turma_id, "materia_id": materia_id})
    
    resultados = []
    for arquivo in arquivos:
        print(f'\n\nEnviando arquivo para iniciar o processamento: {arquivo.filename}')
        resultado = processar_arquivo(arquivo, professor_id, vinculos_processados)
        resultados.append(resultado)
    
    # Retornamos mensagens e códigos HTTP diferentes de acordo com os códigos recebidos nos resultados
    if all(resultado.get('status') == 201 for resultado in resultados):
        message = "Todos os arquivos foram processados com sucesso"
        status_code = 201
    elif all(resultado.get('status') in [400, 500] for resultado in resultados):
        message = "Erro ao processar todos os arquivos"
        status_code = resultados[0].get('status')
    else:
        message = "Alguns arquivos foram processados com sucesso, mas outros falharam"
        status_code = 207
    
    return jsonify({"message": message, "results": resultados}), status_code
