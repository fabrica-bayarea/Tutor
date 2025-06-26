"""
Rotas para lidar com vínculos entre professores, turmas e matérias.
"""

from flask import Blueprint, request, jsonify
from application.services.service_professor import *
from application.services.service_turma import *
from application.services.service_materia import *
from application.services.service_vinculos import *
from application.utils.validacoes import validar_professor
import uuid

professores_turmas_materias_bp = Blueprint('professores_turmas_materias', __name__)

@professores_turmas_materias_bp.route('/professores_turmas_materias/<string:professor_id>', methods=['GET'])
def obter_vinculos_professor_turma_materia(professor_id: uuid.UUID):
    """
    Endpoint para obter os vínculos entre um professor e suas turmas e matérias.

    Espera receber:
    - `professor_id`: uuid.UUID - o ID do professor
    
    1. Valida o professor
    2. Busca os vínculos entre o professor e suas turmas e matérias
    3. Busca os códigos de cada turma e matéria encontrados
    
    Retorna uma lista de dicionários, onde cada dicionário contém os códigos de turma e matéria de um vínculo.
    ```json
    [
        {
            "codigo_turma": "codigo_turma",
            "codigo_materia": "codigo_materia"
        },
        ...
    ]
    ```
    """
    # Valida o professor
    professor_existe = validar_professor(professor_id)
    if not professor_existe:
        return jsonify({"error": f"Professor com ID '{professor_id}' não encontrado"}), 404
    
    # Busca os vínculos
    vinculos = buscar_vinculos_professor_turma_materia(professor_id=professor_id)

    # Busca os códigos de cada turma e matéria encontrados
    codigos_turmas = [buscar_codigo_turma_por_id(vinculo.turma_id) for vinculo in vinculos]
    codigos_materias = [buscar_codigo_materia_por_id(vinculo.materia_id) for vinculo in vinculos]
    
    # Junta corretamente os códigos de cada relação entre turma e matéria em dicionários, dentro de uma lista
    vinculos_processados = [{"codigo_turma": codigo_turma, "codigo_materia": codigo_materia} for codigo_turma, codigo_materia in zip(codigos_turmas, codigos_materias)]
    
    return jsonify(vinculos_processados), 200
