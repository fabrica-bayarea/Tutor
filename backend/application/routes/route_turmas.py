"""
Rotas para lidar com turmas.
"""
from flask import Blueprint, jsonify, request
from application.auth.auth_decorators import token_obrigatorio, apenas_admins
from application.services.service_turma import buscar_turma_por_id, getAllTurmas, createTurma, updateTurma, deleteTurma
from application.models.model_turma import Turma
import uuid
from datetime import datetime

turmas_bp = Blueprint('turmas', __name__)

@turmas_bp.route('/turma/<string:turma_id>', methods=['GET'])
@token_obrigatorio
def obter_turma_por_id(turma_id: uuid.UUID):
    """
    Endpoint para obter uma turma a partir de seu ID.

    Espera receber:
    - `turma_id`: uuid.UUID - o ID da turma
    
    Retorna a turma se ela existir, e None caso contrário.
    """
    try:
        turma = buscar_turma_por_id(turma_id=turma_id)
    except ValueError as e:
        print(f'Erro ao buscar turma: {str(e)}')
        return jsonify({"error": str(e)}), 400
    
    return jsonify(turma), 200


@turmas_bp.route('/admin/turma', methods=['GET'])
@token_obrigatorio
@apenas_admins
def buscar_turmas():

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', type=int)

    query = getAllTurmas(
        codigo= request.args.get('search'),
        semestre = request.args.get('semestre'),
        turno = request.args.get('turno'),
        status = request.args.get('status')
    )


    if limit:
        pagination = query.paginate(page=page, per_page=limit, error_out=False)

        return jsonify({
            "success": True,
            "Turmas": [t.to_dict() for t in pagination.items],
            "pagination": {
                "page": pagination.page,
                "pages": pagination.pages,
                "total": pagination.total
            }
        })

    turmas = query.all()

    return jsonify({
        "success": True,
        "turmas": [t.to_dict() for t in turmas],
        "total": len(turmas)
        })



@turmas_bp.route('/admin/turma', methods=['POST'])
@token_obrigatorio
@apenas_admins
def gerar_turmas():

    dados = request.get_json(silent=True) or {}

    codigo = dados.get('codigo')
    semestre = dados.get('semestre')
    turno = dados.get('turno')


    if not codigo or not semestre or not turno:
        return jsonify({"Error": "Parâmetros 'codigo', 'semestre' e 'turno' são obrigatórios"}), 400
    
    if turno not in ["Matutino", "Vespertino", "Noturno"]: 
        return jsonify({"Error": "Turno deve ser ou Matutino ou Vespertino ou Noturno"}), 400

    existente = Turma.query.filter(
        (Turma.codigo == codigo)
    ).first()

    if existente:
        return jsonify({"Error": "Já existe uma Turma com este código."}), 409

    turma_dict = createTurma(codigo=codigo, semestre=semestre, turno=turno)


    return jsonify(turma_dict), 201



@turmas_bp.route('/admin/turma/<uuid:id>', methods=['PUT'])
@token_obrigatorio
@apenas_admins
def atualizar_turmas(id):

    codigo = request.json.get('codigo')
    semestre = request.json.get('semestre')
    turno = request.json.get('turno')
    status = request.json.get('status')

    if not codigo or not semestre or not turno:
        return jsonify({"Error": "Parâmetros 'codigo', 'semestre' e 'turno' são obrigatórios"}), 400
    
    if turno not in ["Matutino", "Vespertino", "Noturno"]: 
        return jsonify({"Error": "Turno deve ser ou Matutino ou Vespertino ou Noturno"}), 400

    
    if status not in ["ATIVO", "INATIVO"]:
        return jsonify({"error": "Status deve ser ATIVO ou INATIVO"}), 400

    turma_existente = buscar_turma_por_id(id)

    if not turma_existente:
        return jsonify({"Error": "Turma não econtrada"}), 404
    
    turma_nova = updateTurma(id,codigo,semestre,turno,status)

    return jsonify(turma_nova), 200



@turmas_bp.route('/admin/turma/<uuid:id>', methods=['DELETE'])
@token_obrigatorio
@apenas_admins
def deletar_turma(id):
    
    turma, erro = deleteTurma(id)

    if erro:
        if 'turma_nao_encontrada' in erro:
            return jsonify({"error": "Turma não encontrada"}), 404

        if 'turma_vinculada_a_uma_materia' in erro:
            return jsonify({
                "error": "Turma vinculada a Matéria"
            }), 409

        if 'turma_vinculada_a_um_aluno' in erro:
            return jsonify({
                "error": "Turma vinculada um aluno"
            }), 409

    return jsonify({
        "turma": turma.codigo,
        "data_desativacao": datetime.now(),
        "mensagem": "Desativado com sucesso"
    }), 200