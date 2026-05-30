"""
Rotas para lidar com usuários.
"""
import os
from application.config.database import db
from flask import Blueprint, request, jsonify, g
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from application.auth.jwt_handler import gerar_token
from application.auth.auth_decorators import token_obrigatorio, extrair_token, invalidar_token, apenas_admins
from application.services.service_usuario import buscar_aluno, logar_aluno, buscar_professor
from application.models import Usuario

from pathlib import Path
from dotenv import load_dotenv
from flask import make_response

from dotenv import load_dotenv

load_dotenv()

DOMINIO_INSTITUCIONAL = os.getenv("EMAIL_DOMINIO")

usuarios_bp = Blueprint('alunos', __name__)


@usuarios_bp.route('/buscar', methods=['GET'])
def buscarUsuario():
    """
    Endpoint para buscar um usuário.

    Aceita parâmetros via query string ou body JSON:
    - `matricula`: str - o número de matrícula do usuário
    - `nome`: str - o nome do usuário
    - `email`: str - o email do usuário
    - `role`: str - a role do usuário

    Retorna um dicionário contendo as informações do usuário encontrado.
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
    body = request.get_json(silent=True) or {}

    matricula = request.args.get('matricula') or body.get('matricula')
    nome = request.args.get('nome') or body.get('nome')
    email = request.args.get('email') or body.get('email')
    role = request.args.get('role') or body.get('role')

    if not matricula and not role and not nome and not email:
        return jsonify({"error": "Parâmetros de busca são obrigatórios"}), 422

    aluno = buscar_aluno(matricula=matricula, nome=nome, email=email, role=role)

    if not aluno:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return jsonify(aluno), 200


@usuarios_bp.route('/login/google', methods=['POST'])
def login_google():
    """
    Endpoint para autenticação via Google OAuth2.

    Espera receber:
    - `token`: str - o token de ID do Google

    Regras:
    - Não realiza criação de novos usuários.
    - Apenas autentica usuários já existentes no banco.
    - Restringe login ao domínio institucional @iesb.edu.br.

    Retorna um cookie HTTP-only com o JWT e os dados do usuário autenticado.
```json
    {
        "aluno": {
            "id": "id",
            "matricula": "matricula",
            "nome": "nome",
            "email": "email",
            "role": "role do usuario"
        }
    }
```
    """
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

        if not email:
            return jsonify({"error": "Email não encontrado no token"}), 401

        # Restrição ao domínio institucional
        if not email.endswith(DOMINIO_INSTITUCIONAL):
            return jsonify({
                "error": f"Acesso restrito ao domínio {DOMINIO_INSTITUCIONAL}"
            }), 403

        # Busca o usuário existente — não cria novo
        aluno = Usuario.query.filter_by(email=email).first()

        if not aluno:
            return jsonify({
                "error": "Usuário não cadastrado. Entre em contato com a instituição."
            }), 404

        if aluno.status.name != 'ATIVO':
            return jsonify({"error": "Conta desativada. Entre em contato com a instituição."}), 403

        token_jwt = gerar_token(aluno.id, aluno.role.name)

        response = make_response(jsonify({
            "aluno": aluno.to_dict()
        }))

        response.set_cookie(
            "token",
            token_jwt,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60 * 60,
            path="/"
        )

        return response

    except ValueError as e:
        # Captura erros específicos de validação do token Google
        print("ERRO GOOGLE LOGIN - Token inválido:", e)
        return jsonify({"error": "Token inválido ou expirado"}), 401

    except Exception as e:
        print("ERRO GOOGLE LOGIN - Erro inesperado:", e)
        return jsonify({"error": "Erro interno ao processar login"}), 500


@usuarios_bp.route('/login', methods=['POST'])
def login_aluno():
    """
    Endpoint para logar um aluno com matrícula e senha.

    Espera receber:
    - `matricula`: str - o número de matrícula do aluno
    - `senha`: str - a senha do aluno

    Retorna um cookie HTTP-only com o JWT e os dados do aluno logado.
```json
    {
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
    matricula = request.json.get('matricula')
    senha = request.json.get('senha')

    if not matricula or not senha:
        return jsonify({"error": "Parâmetros 'matricula' e 'senha' são obrigatórios"}), 400

    aluno = logar_aluno(matricula, senha)
    if not aluno:
        return jsonify({"error": "Matrícula ou senha inválidos"}), 401

    if aluno.get('status') != 'ATIVO':
        return jsonify({"error": "Conta desativada. Entre em contato com a instituição."}), 403

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
        max_age=60 * 60,
        path="/"
    )

    return response


@usuarios_bp.route('/me', methods=['GET'])
@token_obrigatorio
def me():
    """
    Endpoint para retornar os dados do usuário autenticado.

    Requer cookie HTTP-only com token JWT válido.

    Retorna um dicionário contendo as informações do usuário logado.
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
    usuario = buscar_aluno(g.usuario_id)

    if usuario is None:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return jsonify(usuario)


@usuarios_bp.route('/encerrar-sessao', methods=['POST'])
@token_obrigatorio
def encerrarr_sessao():

    token = extrair_token()

    invalidar_token(token)

    response = jsonify({
        "mensagem": "Sessão encerrada com sucesso"
    })

    response.delete_cookie("token")

    return response, 200


@usuarios_bp.route('/professors', methods=['GET'])
@token_obrigatorio
@apenas_admins
def buscarProfessores():

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', type=int)
    
    professor = buscar_professor(nome = request.args.get('nome'), matricula = request.args.get('matricula'),)
    
    if limit:
            pagination = professor.paginate(page=page, per_page=limit, error_out=False)

            return jsonify({
                "success": True,
                "Professores": [p.to_dict() for p in pagination.items],
                "pagination": {
                    "page": pagination.page,
                    "pages": pagination.pages,
                    "total": pagination.total
                    }
            }), 200
    

    professor = professor.all()

    return jsonify({
        "success": True,
        "Professores": [p.to_dict() for p in professor],
        "total": len(professor)
        }), 200
