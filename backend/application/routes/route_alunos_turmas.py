"""
Rotas para lidar com vínculos entre Alunos e Turmas.
"""
from flask import Blueprint, jsonify
from application.services.service_vinculos import buscar_vinculos_aluno_turma
import uuid

alunos_turmas_bp = Blueprint('alunos_turmas', __name__)

@alunos_turmas_bp.route('/aluno/<string:aluno_id>', methods=['GET'])
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

@alunos_turmas_bp.route('/turma/<string:turma_id>', methods=['GET'])
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
