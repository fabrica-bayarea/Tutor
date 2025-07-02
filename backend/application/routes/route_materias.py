"""
Rotas para lidar com matérias.
"""
from flask import Blueprint, jsonify
from application.services.service_materia import buscar_materia_por_id
import uuid

materias_bp = Blueprint('materias', __name__)

@materias_bp.route('/materia/<string:materia_id>', methods=['GET'])
def obter_materia_por_id(materia_id: uuid.UUID):
    """
    Endpoint para obter uma matéria a partir de seu ID.

    Espera receber:
    - `materia_id`: uuid.UUID - o ID da matéria
    
    Retorna a matéria se ela existir, e None caso contrário.
    """
    try:
        materia = buscar_materia_por_id(materia_id=materia_id)
    except ValueError as e:
        print(f'Erro ao buscar matéria: {str(e)}')
        return jsonify({"error": str(e)}), 400
    
    return jsonify(materia), 200
