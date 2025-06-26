"""
Rotas para lidar com professores.
"""
from flask import Blueprint, request, jsonify
from application.auth.jwt_handler import gerar_token
from application.services.service_professor import *
from application.services.service_turma import *
from application.services.service_materia import *
from application.services.service_vinculos import *

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/login', methods=['POST'])
def login_professor():
    """
    Endpoint para logar um professor.

    Espera receber:
    - `matricula`: str - o número de matrícula do professor
    - `senha`: str - a senha do professor
    
    Retorna um dicionário contendo o token JWT e as informações do professor logado.
    """
    # Verifica se os dados necessários estão presentes
    matricula = request.json.get('matricula')
    senha = request.json.get('senha')
    
    if not matricula or not senha:
        return jsonify({"error": "Parâmetros 'matricula' e 'senha' são obrigatórios"}), 400
    
    # Verifica se existe um professor com esses dados
    professor = logar_professor(matricula, senha)
    if not professor:
        return jsonify({"error": "Matrícula ou senha inválidos"}), 401
    
    # Gera um token JWT
    token = gerar_token(professor['id'], role="professor")

    # Retorna o token JWT e os dados do professor
    return jsonify({
        "token": token,
        "professor": professor
    }), 200
