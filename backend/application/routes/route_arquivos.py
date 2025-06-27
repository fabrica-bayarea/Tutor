"""
Rotas para lidar com arquivos.
"""
from flask import Blueprint, request, jsonify, g
import uuid
import json
from application.auth import token_obrigatorio
from application.services.service_arquivo import processar_arquivo, obter_arquivos_turma_materia
from application.utils.validacoes import validar_professor_turma_materia

arquivos_bp = Blueprint('arquivos', __name__)

@arquivos_bp.route('/upload', methods=['POST'])
@token_obrigatorio
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
