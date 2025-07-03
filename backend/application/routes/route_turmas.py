"""
Rotas para lidar com turmas.
"""
from flask import Blueprint, jsonify
from application.auth.auth_decorators import token_obrigatorio
from application.services.service_turma import buscar_turma_por_id
import uuid

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
