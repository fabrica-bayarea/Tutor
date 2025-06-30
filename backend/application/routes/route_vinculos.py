"""
Rotas para lidar com todos os tipos de vínculos entre tabelas intermediárias.
"""
from flask import Blueprint, request, jsonify, g
from application.auth.auth_decorators import token_obrigatorio, apenas_professores, apenas_alunos
from application.services.service_vinculos import criar_vinculo_aluno_turma, buscar_vinculos_aluno_turma, buscar_vinculos_professor_turma_materia, buscar_vinculos_arquivo_turma_materia, buscar_vinculos_turma_materia
from application.utils.validacoes import validar_professor_turma_materia
import uuid

vinculos_bp = Blueprint('vinculos', __name__)

# -------------------- ALUNO <-> TURMA --------------------

@vinculos_bp.route('/alunos_turmas', methods=['POST'])
@token_obrigatorio
#@apenas_alunos
def novo_vinculo_aluno_turma():
    """
    Endpoint para criar um novo vínculo entre um aluno e uma turma.

    Espera receber todos esses dois parâmetros:
    - `aluno_id`: uuid.UUID - o ID do aluno
    - `turma_id`: uuid.UUID - o ID da turma

    Retorna True se o vínculo for criado com sucesso, e False se o vínculo já existir.
    """
    # Verifica se os dados necessários estão presentes
    aluno_id = request.json.get('aluno_id')
    turma_id = request.json.get('turma_id')

    if not aluno_id or not turma_id:
        return jsonify({"error": "É obrigatório fornecer um ID de aluno e um ID de turma."}), 400
    
    try:
        novo_vinculo = criar_vinculo_aluno_turma(aluno_id, turma_id)
        if not novo_vinculo:
            return jsonify({"message": "Vínculo já existe."}), 400
        
        return jsonify({"message": f"Vínculo entre aluno '{aluno_id}' e turma '{turma_id}' criado com sucesso."}), 201
    except ValueError as e:
        print(f'Erro ao criar vínculo AlunoTurma: {str(e)}')
        return jsonify({"error": str(e)}), 400

@vinculos_bp.route('/alunos_turmas/aluno/<string:aluno_id>', methods=['GET'])
@token_obrigatorio
@apenas_alunos
def obter_vinculos_aluno_turma(aluno_id: uuid.UUID):
    """
    Endpoint para obter TODOS os vínculos entre um aluno e suas turmas.

    Espera receber:
    - `aluno_id`: uuid.UUID - o ID do aluno
    
    Retorna uma lista de vínculos AlunoTurma que correspondem aos filtros.
    Se nenhum parâmetro for fornecido, retorna None.
    """
    try:
        vinculos = buscar_vinculos_aluno_turma(aluno_id=aluno_id)
    except ValueError as e:
        print(f'Erro ao buscar vínculos AlunoTurma: {str(e)}')
        return jsonify({"error": str(e)}), 400
    
    return jsonify(vinculos), 200

@vinculos_bp.route('/alunos_turmas/turma/<string:turma_id>', methods=['GET'])
@token_obrigatorio
#@apenas_professores
def obter_vinculos_turma_aluno(turma_id: uuid.UUID):
    """
    Endpoint para obter TODOS os vínculos entre uma turma e seus alunos.

    Espera receber:
    - `turma_id`: uuid.UUID - o ID da turma
    
    Retorna uma lista de vínculos AlunoTurma que correspondem aos filtros.
    Se nenhum parâmetro for fornecido, retorna None.
    """
    try:
        vinculos = buscar_vinculos_aluno_turma(turma_id=turma_id)
    except ValueError as e:
        print(f'Erro ao buscar vínculos AlunoTurma: {str(e)}')
        return jsonify({"error": str(e)}), 400
    
    return jsonify(vinculos), 200

# -------------------- TURMA <-> MATÉRIA --------------------

@vinculos_bp.route('/turmas_materias', methods=['POST'])
@token_obrigatorio
@apenas_professores
def novo_vinculo_turma_materia():
    """
    Endpoint para criar um novo vínculo entre uma turma e uma matéria.

    Espera receber todos esses dois parâmetros:
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna True se o vínculo for criado com sucesso, e False se o vínculo já existir.
    """
    # Verifica se os dados necessários estão presentes
    turma_id = request.json.get('turma_id')
    materia_id = request.json.get('materia_id')

    if not turma_id or not materia_id:
        return jsonify({"error": "É obrigatório fornecer um ID de turma e um ID de matéria."}), 400
    
    try:
        novo_vinculo = criar_vinculo_turma_materia(turma_id, materia_id)
        if not novo_vinculo:
            return jsonify({"message": "Vínculo já existe."}), 400
        
        return jsonify({"message": f"Vínculo entre turma '{turma_id}' e matéria '{materia_id}' criado com sucesso."}), 201
    except ValueError as e:
        print(f'Erro ao criar vínculo TurmaMateria: {str(e)}')
        return jsonify({"error": str(e)}), 400

@vinculos_bp.route('/turmas_materias/turma/<string:turma_id>', methods=['GET'])
@token_obrigatorio
def obter_vinculos_turma_materia(turma_id: uuid.UUID):
    """
    Endpoint para obter TODOS os vínculos entre uma turma e suas matérias.

    Espera receber:
    - `turma_id`: uuid.UUID - o ID da turma
    
    Retorna uma lista de vínculos TurmaMateria que correspondem aos filtros.
    Se nenhum parâmetro for fornecido, retorna None.
    """
    try:
        vinculos = buscar_vinculos_turma_materia(turma_id=turma_id)
    except ValueError as e:
        print(f'Erro ao buscar vínculos TurmaMateria: {str(e)}')
        return jsonify({"error": str(e)}), 400
    
    return jsonify(vinculos), 200

@vinculos_bp.route('/turmas_materias/materia/<string:materia_id>', methods=['GET'])
@token_obrigatorio
@apenas_professores
def obter_vinculos_materia_turma(materia_id: uuid.UUID):
    """
    Endpoint para obter TODOS os vínculos entre uma matéria e suas turmas.

    Espera receber:
    - `materia_id`: uuid.UUID - o ID da matéria
    
    Retorna uma lista de vínculos TurmaMateria que correspondem aos filtros.
    Se nenhum parâmetro for fornecido, retorna None.
    """
    try:
        vinculos = buscar_vinculos_turma_materia(materia_id=materia_id)
    except ValueError as e:
        print(f'Erro ao buscar vínculos TurmaMateria: {str(e)}')
        return jsonify({"error": str(e)}), 400
    
    return jsonify(vinculos), 200

# -------------------- PROFESSOR <-> TURMA <-> MATÉRIA --------------------

@vinculos_bp.route('/professores_turmas_materias', methods=['POST'])
@token_obrigatorio
@apenas_professores
def novo_vinculo_professor_turma_materia():
    """
    Endpoint para criar um novo vínculo entre um professor, uma turma e uma matéria.

    Espera receber todos esses três parâmetros:
    - `professor_id`: uuid.UUID - o ID do professor
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna True se o vínculo for criado com sucesso, e False se o vínculo já existir.
    """
    # Verifica se os dados necessários estão presentes
    professor_id = request.json.get('professor_id')
    turma_id = request.json.get('turma_id')
    materia_id = request.json.get('materia_id')

    if not professor_id or not turma_id or not materia_id:
        return jsonify({"error": "É obrigatório fornecer um ID de professor, um ID de turma e um ID de matéria."}), 400
    
    try:
        novo_vinculo = criar_vinculo_professor_turma_materia(professor_id, turma_id, materia_id)
        if not novo_vinculo:
            return jsonify({"message": "Vínculo já existe."}), 400
        
        return jsonify({"message": f"Vínculo entre professor '{professor_id}', turma '{turma_id}' e matéria '{materia_id}' criado com sucesso."}), 201
    except ValueError as e:
        print(f'Erro ao criar vínculo ProfessorTurmaMateria: {str(e)}')
        return jsonify({"error": str(e)}), 400

@vinculos_bp.route('/professores_turmas_materias/professor/<string:professor_id>', methods=['GET'])
@token_obrigatorio
@apenas_professores
def obter_vinculos_professor_turma_materia(professor_id: uuid.UUID):
    """
    Endpoint para obter TODOS os vínculos entre um professor e suas turmas e matérias.

    Espera receber:
    - `professor_id`: uuid.UUID - o ID do professor
    
    Retorna uma lista de vínculos ProfessorTurmaMateria que correspondem aos filtros.
    Se nenhum parâmetro for fornecido, retorna None.
    """
    try:
        vinculos = buscar_vinculos_professor_turma_materia(professor_id=professor_id)
    except ValueError as e:
        print(f'Erro ao buscar vínculos ProfessorTurmaMateria: {str(e)}')
        return jsonify({"error": str(e)}), 400
    
    return jsonify(vinculos), 200

# -------------------- ARQUIVO <-> TURMA <-> MATÉRIA --------------------

@vinculos_bp.route('/arquivos_turmas_materias', methods=['POST'])
@token_obrigatorio
#@apenas_professores
def novo_vinculo_arquivo_turma_materia():
    """
    Endpoint para criar um novo vínculo entre um arquivo, uma turma e uma matéria.

    Espera receber todos esses três parâmetros:
    - `arquivo_id`: uuid.UUID - o ID do arquivo
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna True se o vínculo for criado com sucesso, e False se o vínculo já existir.
    """
    # Verifica se os dados necessários estão presentes
    arquivo_id = request.json.get('arquivo_id')
    turma_id = request.json.get('turma_id')
    materia_id = request.json.get('materia_id')

    if not arquivo_id or not turma_id or not materia_id:
        return jsonify({"error": "É obrigatório fornecer um ID de arquivo, um ID de turma e um ID de matéria."}), 400
    
    try:
        novo_vinculo = criar_vinculo_arquivo_turma_materia(arquivo_id, turma_id, materia_id)
        if not novo_vinculo:
            return jsonify({"message": "Vínculo já existe."}), 400
        
        return jsonify({"message": f"Vínculo entre arquivo '{arquivo_id}', turma '{turma_id}' e matéria '{materia_id}' criado com sucesso."}), 201
    except ValueError as e:
        print(f'Erro ao criar vínculo ArquivoTurmaMateria: {str(e)}')
        return jsonify({"error": str(e)}), 400

@vinculos_bp.route('/arquivos_turmas_materias/<string:turma_id>_<string:materia_id>', methods=['GET'])
@token_obrigatorio
@apenas_professores
def obter_vinculos_arquivo_turma_materia(turma_id: uuid.UUID, materia_id: uuid.UUID):
    """
    Endpoint para obter vínculos dos arquivos de uma matéria em uma turma.

    Espera receber:
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    1. Valida o professor
    2. Busca os vínculos entre arquivos, turmas e matérias
    
    Retorna os vínculos encontrados.
    """
    # Valida se o professor tem vínculo com a turma e matéria
    if not validar_professor_turma_materia(g.usuario_id, turma_id, materia_id):
        return jsonify({"error": "Acesso não autorizado para esta turma/matéria"}), 403

    # Busca os vínculos
    try:
        vinculos = buscar_vinculos_arquivo_turma_materia(turma_id=turma_id, materia_id=materia_id)
    except ValueError as e:
        print(f'Erro ao buscar vínculos: {str(e)}')
        return jsonify({"error": str(e)}), 400

    # Retorna os vínculos encontrados
    return jsonify(vinculos), 200
