"""
Rotas para lidar com professores.
"""
from flask import Blueprint, request, jsonify
from application.auth.jwt_handler import gerar_token
from application.services.service_professor import criar_professor, buscar_professor, logar_professor

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/criar', methods=['POST'])
def gerar_professor():
    """
    Endpoint para criar um professor.

    Espera receber:
    - `matricula`: str - o número de matrícula do professor
    - `nome`: str - o nome do professor
    - `email`: str - o email do professor
    - `senha`: str - a senha do professor
    - `cpf`: str - o cpf do professor
    - `data_nascimento`: str - a data de nascimento do professor
    
    Retorna um dicionário contendo as informações do professor criado.
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
    
    # Verifica se já existe um professor com alguns dados que devem ser únicos
    professor_existe = buscar_professor(matricula=matricula, email=email, cpf=cpf)
    if professor_existe:
        return jsonify({"error": "Professor com essa matrícula, email ou cpf já existe"}), 400
    
    # Cria o professor
    professor = criar_professor(matricula, nome, email, senha, cpf, data_nascimento)
    return jsonify(professor), 201

@professores_bp.route('/login', methods=['POST'])
def login_professor():
    """
    Endpoint para logar um professor.

    Espera receber:
    - `matricula`: str - o número de matrícula do professor
    - `senha`: str - a senha do professor
    
    Retorna um dicionário contendo o token JWT e as informações do professor logado.
    ```json
    {
        "token": "token",
        "professor": {
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
