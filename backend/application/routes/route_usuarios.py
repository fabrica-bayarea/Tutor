"""
Rotas para lidar com alunos.
"""
import os
import secrets
from application.config.database import db
from flask import Blueprint, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from application.auth.jwt_handler import gerar_token
from application.auth.auth_decorators import apenas_admins, token_obrigatorio
from application.services.service_usuario import criar_aluno, buscar_aluno, logar_aluno, alterar_aluno
from application.models import Usuario
from application.models.model_usuario import RoleEnum  

from pathlib import Path
from dotenv import load_dotenv
from flask import make_response

dotenv_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path)

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
    
    existente = Usuario.query.filter(
        (Usuario.matricula == matricula) | (Usuario.email == email)
    ).first()

    if existente:
        return jsonify({"error": "Email ou matrícula já cadastrados."}), 409

    # Verifica se já existe um aluno com alguns dados que devem ser únicos
    aluno_existe = buscar_aluno(matricula=matricula, email=email)
    if aluno_existe:
        print('ca')
        return jsonify({"error": "Aluno com essa matrícula ou email já existe"}), 409
    
    # Cria o aluno
    aluno = criar_aluno(matricula, nome, email, senha)
    return jsonify(aluno), 201

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

    if not token:
        return jsonify({"error": "Token não enviado"}), 400

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            grequests.Request(),
            os.getenv("GOOGLE_CLIENT_ID"),
            clock_skew_in_seconds=10 
        )

        email = idinfo.get('email')
        nome = idinfo.get('name')
        sub = idinfo.get('sub')

        if not email:
            return jsonify({"error": "Email não encontrado no token"}), 401

        aluno = Usuario.query.filter_by(email=email).first()

        if not aluno:
            aluno = Usuario(
                matricula=f"G{sub[-8:]}",
                nome=nome,
                email=email,
                senha=secrets.token_urlsafe(16),
                role=RoleEnum.ALUNO
            )
            db.session.add(aluno)
            db.session.commit()

        token_jwt = gerar_token(aluno.id, aluno.role.value)
        
        response = make_response(jsonify({
            "aluno": aluno.to_dict()
        }))

        response.set_cookie(
            "token",
            token_jwt,
            httponly=True,
            secure=False,  
            samesite="Lax",
            max_age=60,
            path="/"
        )

        return response

    except Exception as e:
        print("ERRO GOOGLE LOGIN:", e)
        return jsonify({"error": "Token inválido"}), 401
    
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
    
    # Gera o token
    token = gerar_token(aluno['id'], aluno['role'])

    response = make_response(jsonify({
        "aluno": aluno
    }))

    response.set_cookie(
        "token",
        token,
        httponly=True,
        secure=False,  
        samesite="Lax",  
        max_age=60,
        path="/"
    )

    return response

@usuarios_bp.route('/me', methods=['GET'])
@token_obrigatorio
def me():
    usuario = buscar_aluno(g.usuario_id)

    if usuario == None: return jsonify({"error": "Usuário não encontrado"}), 404
       
    return jsonify(usuario)
