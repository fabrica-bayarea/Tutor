from flask import Blueprint, jsonify, g
from application.auth.auth_decorators import token_obrigatorio
from application.services.service_data import buscar_materias_user, buscar_turmas_user

data_bp = Blueprint('data', __name__)

@data_bp.route('/materias', methods=['GET'])
@token_obrigatorio
def obter_materias_user():
    try:
        user_id = g.usuario_id
        materias = buscar_materias_user(user_id=user_id)
    except ValueError as e:
        print(f'Erro ao buscar matérias: {str(e)}')
        return jsonify({"error": str(e)}), 400
    
    return jsonify(materias), 200

@data_bp.route('/turmas', methods=['GET'])
@token_obrigatorio
def obter_turmas_user():
    try:
        user_id = g.usuario_id
        turmas = buscar_turmas_user(user_id=user_id)
    except ValueError as e:
        print(f'Erro ao buscar turmas: {str(e)}')
        return jsonify({"error": str(e)}), 400
    
    return jsonify(turmas), 200
