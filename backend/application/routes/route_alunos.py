"""
Rotas para lidar com alunos.
"""
from flask import Blueprint, request, jsonify
from application.auth.jwt_handler import gerar_token
from application.services.service_aluno import criar_aluno, buscar_aluno, logar_aluno

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/criar', methods=['POST'])
def gerar_aluno():
    """
    Endpoint para criar um aluno.

    Espera receber:
    - `matricula`: str - o número de matrícula do aluno
    - `nome`: str - o nome do aluno
    - `email`: str - o email do aluno
    - `senha`: str - a senha do aluno
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
    # Verifica se os dados necessários estão presentes
    matricula = request.json.get('matricula')
    nome = request.json.get('nome')
    email = request.json.get('email')
    senha = request.json.get('senha')
    cpf = request.json.get('cpf')
    data_nascimento = request.json.get('data_nascimento')
    
    if not matricula or not nome or not email or not senha or not cpf or not data_nascimento:
        return jsonify({"error": "Parâmetros 'matricula', 'nome', 'email', 'cpf', 'data_nascimento' e 'senha' são obrigatórios"}), 400
    
    # Verifica se já existe um aluno com alguns dados que devem ser únicos
    aluno_existe = buscar_aluno(matricula=matricula, email=email, cpf=cpf)
    if aluno_existe:
        return jsonify({"error": "Aluno com essa matrícula, email ou cpf já existe"}), 400
    
    # Cria o aluno
    aluno = criar_aluno(matricula, nome, email, senha, cpf, data_nascimento)
    return jsonify(aluno), 201

@alunos_bp.route('/login', methods=['POST'])
def login_aluno():
    """
    Endpoint para logar um aluno.

    Espera receber:
    - `matricula`: str - o número de matrícula do aluno
    - `senha`: str - a senha do aluno
    
    Retorna um dicionário contendo o token JWT e as informações do aluno logado.
    ```json
    {
        "token": "token",
        "aluno": {
            "id": "id",
            "matricula": "matricula",
            "nome": "nome",
            "email": "email",
            "cpf": "cpf",
            "data_nascimento": "data_nascimento"
        }
    }
    ```
    """
    # Verifica se os dados necessários estão presentes
    matricula = request.json.get('matricula')
    senha = request.json.get('senha')
    
    if not matricula or not senha:
        return jsonify({"error": "Parâmetros 'matricula' e 'senha' são obrigatórios"}), 400
    
    # Verifica se existe um aluno com esses dados
    aluno = logar_aluno(matricula, senha)
    if not aluno:
        return jsonify({"error": "Matrícula ou senha inválidos"}), 401
    
    # Gera um token JWT
    token = gerar_token(aluno['id'], role="aluno")
    
    # Retorna o token JWT e as informações do aluno
    return jsonify({
        "token": token,
        "aluno": aluno
    }), 200
