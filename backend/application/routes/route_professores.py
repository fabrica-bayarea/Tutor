"""
Rotas para lidar com professores.
"""
from flask import Blueprint, request, jsonify
from application.services.service_professor import *
from application.services.service_turma import *
from application.services.service_materia import *
from application.services.service_vinculos import *

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/turmas_materias/<string:matricula_professor>', methods=['GET'])
def obter_vinculos_professor_turma_materia(matricula_professor: str):
    """
    Endpoint para obter os vínculos entre um professor e suas turmas e matérias.

    Espera receber:
    - `matricula_professor`: str - o número de matrícula do professor
    
    1. Busca o ID do professor no banco de dados
    2. Usa o ID do professor para buscar os vínculos entre ele e suas turmas e matérias
    3. Usa os IDs de cada turma e matéria encontrados para buscar os códigos de cada uma
    
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
    professor_id = buscar_id_professor_por_matricula(matricula_professor)
    if not professor_id:
        return jsonify({"error": f"Professor com matrícula '{matricula_professor}' não encontrado"}), 404
    
    # Busca os vínculos
    vinculos = buscar_vinculos_professor_turma_materia(professor_id=professor_id)

    # Busca os códigos de cada turma e matéria encontrados
    codigos_turmas = [buscar_codigo_turma_por_id(vinculo.turma_id) for vinculo in vinculos]
    codigos_materias = [buscar_codigo_materia_por_id(vinculo.materia_id) for vinculo in vinculos]
    
    # Junta corretamente os códigos de cada relação entre turma e matéria em dicionários, dentro de uma lista
    vinculos_processados = [{"codigo_turma": codigo_turma, "codigo_materia": codigo_materia} for codigo_turma, codigo_materia in zip(codigos_turmas, codigos_materias)]
    
    return jsonify(vinculos_processados), 200
