"""
Rotas para lidar com alunos.
"""
from flask import Blueprint, request, jsonify
from application.services.service_aluno import *

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/criar', methods=['POST'])
def criar_aluno():
    """
    Endpoint para criar um aluno.

    Espera receber:
    - `matricula`: str - o número de matrícula do aluno
    - `nome`: str - o nome do aluno
    - `email`: str - o email do aluno
    - `cpf`: str - o cpf do aluno
    - `data_nascimento`: str - a data de nascimento do aluno
    
    Retorna um dicionário contendo as informações do aluno criado.
    ```json
    {
        "id": "id",
        "matricula": "matricula",
        "nome": "nome",
        "email": "email",
        "cpf": "cpf",
        "data_nascimento": "data_nascimento"
    }
    ```
    """
    matricula = request.form.get('matricula')
    nome = request.form.get('nome')
    email = request.form.get('email')
    cpf = request.form.get('cpf')
    data_nascimento = request.form.get('data_nascimento')
    
    if not matricula or not nome or not email or not cpf or not data_nascimento:
        return jsonify({"error": "Parâmetros 'matricula', 'nome', 'email', 'cpf' e 'data_nascimento' são obrigatórios"}), 400
    
    aluno = criar_aluno(matricula, nome, email, cpf, data_nascimento)
    return jsonify(aluno)
