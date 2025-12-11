"""
Rotas para lidar com alunos.
"""
import os
from flask import Blueprint, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from application.auth.jwt_handler import gerar_token
from application.auth.auth_decorators import apenas_admins, token_obrigatorio
from application.services.service_usuario import criar_aluno, buscar_aluno, logar_aluno, alterar_aluno

usuarios_bp = Blueprint('alunos', __name__)

@usuarios_bp.route('/criar', methods=['POST'])
def gerar_aluno():
    """
    Endpoint para criar um aluno.

    Espera receber:
    - `matricula`: str - o número de matrícula do aluno
    - `nome`: str - o nome do aluno
    - `email`: str - o email do aluno
    - `senha`: str - a senha do aluno
    
    Retorna um dicionário contendo as informações do aluno criado.
    ```json
    {
        "id": "id",
        "matricula": "matricula",
        "nome": "nome",
        "email": "email",
        "role": "role do usuario"
    }
    ```
    """
    # Verifica se os dados necessários estão presentes
    matricula = request.json.get('matricula')
    nome = request.json.get('nome')
    email = request.json.get('email')
    senha = request.json.get('senha')
    
    if not matricula or not nome or not email or not senha:
        return jsonify({"error": "Parâmetros 'matricula', 'nome', 'email' e 'senha' são obrigatórios"}), 400
    
    # Verifica se já existe um aluno com alguns dados que devem ser únicos
    aluno_existe = buscar_aluno(matricula=matricula, email=email)
    if aluno_existe:
        return jsonify({"error": "Aluno com essa matrícula ou email já existe"}), 409
    
    # Cria o aluno
    aluno = criar_aluno(matricula, nome, email, senha)
    return jsonify(aluno), 201

@usuarios_bp.route('/login', methods=['POST'])
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
            "role": "role do usuario(1,2,3)"
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
    token = gerar_token(aluno['id'], aluno[role])
    
    # Retorna o token JWT e as informações do aluno
    return jsonify({
        "token": token,
        "aluno": aluno
    }), 200

@usuarios_bp.route('/alterar', methods=['PUT'])
@token_obrigatorio
@apenas_admins
def elegerUsuario():
    """
    Endpoint para editar um usuario.

    Espera receber:
    - `matricula`: str - o número de matrícula do usuario
    - `role`: str - role nova do usuario
    
    Retorna um dicionário contendo as informações do aluno alterado.
    ```json
    {
        "id": "id",
        "matricula": "matricula",
        "nome": "nome",
        "email": "email",
        "role": "role do usuario"
    }
    ```
    """

    # Verifica se os dados necessários estão presentes
    matricula = request.json.get('matricula')
    role = request.json.get('role')

        
    if not matricula or not role:
        return jsonify({"error": "Parâmetros 'matricula' e 'role' são obrigatórios"}), 400

    aluno_existe = buscar_aluno(matricula=matricula)

    if not aluno_existe:
        return jsonify({"error": "Matrícula não encontrada"}), 404

    aluno = alterar_aluno(matricula,role)
    return jsonify(aluno), 200        

@usuarios_bp.route('/buscar',methods=['GET'])
def buscarUsuario():

    matricula = request.json.get('matricula')
    nome: request.json.get('nome')
    email: request.json.get('email')
    role = request.json.get('role')

    if not matricula and not role and not nome and not email:
        return jsonify({"error": "Parâmetros de busca são obrigatórios"}), 422
    
    aluno = buscar_aluno(matricula=matricula,nome=nome,email=email,role=role)

    if not aluno:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return jsonify(aluno), 200

@usuarios_bp.route('/login/google', methods=['POST'])
def login_google():
    data = request.json
    token = data.get('token')
    
    try:
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), os.getenv("GOOGLE_CLIENT_ID"))

        email = idinfo['email']
        nome = idinfo['name']
        sub = idinfo['sub']

        aluno = Usuario.query.filter_by(email=email).first()

        if not aluno:
            matricula = f"G{sub}"
            senha = secrets.token_urlsafe(8)

            aluno = Usuario(
                matricula=matricula,
                nome=nome,
                email=email,
                senha=senha,
                role=RoleEnum.ALUNO
            )
            db.session.add(aluno)
            db.session.commit()

        token_jwt = gerar_token(aluno.id, aluno.role.value)

        return jsonify({
            "aluno": aluno.to_dict(),
            "token": token_jwt
        }), 200

    except ValueError:
        return jsonify({"error": "Token inválido"}), 401