"""
Rotas para lidar com admin.
"""
from flask import Blueprint, jsonify, current_app, request
from application.auth.auth_decorators import token_obrigatorio
import uuid
from application.models.model_usuario import RoleEnum, Usuario
from application.models.model_turma import Turma
from application.services.service_usuario import (criar_usuario, buscar_aluno, desativar_aluno, alterar_aluno_por_id, reativar_aluno, buscar_alunos_por_filtro)
import secrets
from application.config.database import db
from datetime import datetime
from application.libs.email_sender import enviar_email_convite
from flask import make_response
from application.auth.jwt_handler import gerar_token
from application.services.service_usuario import definir_senha_primeiro_acesso, _validar_forca_senha

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/usuarios/all', methods=['GET'])
def listar_todos_usuarios():
    """
    Endpoint para listar usuarios

    Espera receber algum desses ou nenhum:
    - `matricula`: str - o número de matrícula do aluno
    - `nome`: str - o nome do aluno
    - `email`: str - o email do aluno
    - `status`: str - o status do aluno
    - `role`: str - a role do aluno
    
    Retorna um dicionário contendo as informações do aluno(s)
    ```json
    {
        "id": "id",
        "matricula": "matricula",
        "nome": "nome",
        "email": "email",
        "role": "role do usuario"
        "status": "status do usuario"
    }
    ```
    """
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', type=int)

        query = buscar_alunos_por_filtro(
            nome = request.args.get('nome'),
            matricula = request.args.get('matricula'),
            role = request.args.get('role'),
            status = request.args.get('status'),
            turma =request.args.get('turma')
        )

        if limit:
            pagination = query.paginate(page=page, per_page=limit, error_out=False)

            return jsonify({
                "success": True,
                "usuarios": [u.to_dict() for u in pagination.items],
                "pagination": {
                    "page": pagination.page,
                    "pages": pagination.pages,
                    "total": pagination.total
                }
            })

        usuarios = query.all()

        return jsonify({
            "success": True,
            "usuarios": [u.to_dict() for u in usuarios],
            "total": len(usuarios)
        })

    except Exception as e:
        return jsonify({
            "succe": False,
            "message": str(e)
        }), 500


    
@admin_bp.route('/usuarios/criar', methods=['POST'])
def gerar_aluno():
    """
    Endpoint para criar um usuário e disparar e-mail de convite.

    Espera receber:
    - `matricula`: str - o número de matrícula do usuário
    - `nome`: str - o nome do usuário
    - `email`: str - o e-mail institucional do usuário
    - `via_google`: bool (opcional) - se True, ignora o fluxo de convite por e-mail

    Retorna um dicionário contendo as informações do usuário criado.
```json
    {
        "id": "id",
        "matricula": "matricula",
        "nome": "nome",
        "email": "email",
        "role": "role do usuario",
        "status": "status do usuario"
    }
```
    """
    dados = request.get_json(silent=True) or {}

    matricula = dados.get('matricula')
    nome = dados.get('nome')
    email = dados.get('email')
    via_google = dados.get('via_google', False)

    if not matricula or not nome or not email:
        return jsonify({"error": "Parâmetros 'matricula', 'nome' e 'email' são obrigatórios"}), 400

    if not email.endswith("@iesb.edu.br"):
        return jsonify({"error": "Email deve ser institucional (@iesb.edu.br)"}), 400

    existente = Usuario.query.filter(
        (Usuario.matricula == matricula) | (Usuario.email == email)
    ).first()

    if existente:
        return jsonify({"error": "Email ou matrícula já cadastrados."}), 409

    usuario_dict, token = criar_usuario(matricula, nome, email, via_google)

    if not via_google and token:
        try:
            enviar_email_convite(email, nome, token)
        except Exception as e:
            current_app.logger.error(f"Erro ao enviar e-mail de convite para {email}: {e}")

    return jsonify(usuario_dict), 201


@admin_bp.route("/usuarios/delete/<uuid:id>", methods=['DELETE'])
def deletar_usuario(id):
    """
    Endpoint para deletar(Inativar) usuario por id

    Espera receber algum desses ou nenhum:
    - `id`: str - O uuid do aluno
    
    Retorna um dicionário contendo as informações do aluno(s)
    ```json
    {
        "Data de desativação: ": "data da hora da desativação do aluno",
        "Matricula:": "matricula do aluno",
        "Usuario:": "nome do aluno",
        "mensagem": "Desativado com sucesso"
    }
    ```
    """
    aluno = desativar_aluno(id)

    if not aluno:
        return jsonify({"error": "Usuario não encontrado"}), 404

    return jsonify({
        "Usuario:": aluno.nome,
        "Matricula:": aluno.matricula,
        "Data de desativação: ": datetime.now(),
        "mensagem": "Desativado com sucesso"
    }), 200



@admin_bp.route("/usuarios/<uuid:id>", methods=['GET'])
def buscar_alunos_por_id(id):
    """
    Endpoint para buscar usuario por id

    Espera receber algum desses ou nenhum:
    - `id`: str - O uuid do aluno
    
    Retorna um dicionário contendo as informações do aluno(s)
    ```json
    {
        "id": "id",
        "matricula": "matricula",
        "nome": "nome",
        "email": "email",
        "role": "role do usuario"
        "status": "status do usuario"
    }
    ```
    """
    aluno = buscar_aluno(id)

    return jsonify(aluno), 200


@admin_bp.route("/usuarios/<uuid:id>", methods=['PUT'])
def atualizar_aluno_por_id(id):
    """
    Endpoint para atualizar usuario por id

    Espera receber:
    - `matricula`: str - o número de matrícula do aluno
    - `nome`: str - o nome do aluno
    - `email`: str - o email do aluno
    - `status`: str - o status do aluno
    - `role`: str - a role do aluno
    
    Retorna um dicionário contendo as informações do aluno(s)
    ```json
    {
        "id": "id",
        "matricula": "matricula",
        "nome": "nome",
        "email": "email",
        "role": "role do usuario"
        "status": "status do usuario"
    }
    ```
    """
    matricula = request.json.get('matricula')
    nome = request.json.get('nome')
    email = request.json.get('email')
    role = request.json.get('role')
    status = request.json.get('status')

    if not email.endswith("@iesb.edu.br"):
        return jsonify({"error": "Email deve ser institucional (@iesb.edu.br)"}), 400
    
    if status not in ["ATIVO", "INATIVO"]:
        return jsonify({"error": "Status deve ser ATIVO ou INATIVO"}), 400

    aluno_existente = buscar_aluno(id)

    if not aluno_existente:
        return jsonify({"error: Usuario não encontrado"}), 404
    
    aluno_novo = alterar_aluno_por_id(id, matricula, nome, email, status, role)

    return jsonify(aluno_novo), 200



@admin_bp.route("/usuarios/<uuid:id>/reativar", methods=['PATCH'])
def reativar_usuario(id):
    """
    Endpoint para reativar usuario por id

    Espera receber:
    - `id`: str - O uuid do aluno
    
    Retorna um dicionário contendo as informações do aluno(s)
    ```json
    {
        "id": "id",
        "matricula": "matricula",
        "nome": "nome",
        "email": "email",
        "role": "role do usuario"
        "status": "status do usuario"
    }
    ```
    """
    status = request.json.get('status')

    if status not in ["ATIVO"]:
        return jsonify({"error": "Status deve ser ATIVO ou INATIVO"}), 400
    
    aluno_existente = buscar_aluno(id)

    if not aluno_existente:
        return jsonify({"error: Usuario não encontrado"}), 404
    
    aluno = reativar_aluno(id, status)

    return jsonify({
        "Usuario:": aluno["nome"],
        "Matricula:": aluno["matricula"],
        "Data de reativação: ": datetime.now(),
        "mensagem": "Ativado com sucesso"
    }), 200

@admin_bp.route('/usuarios/recriar_senha', methods=['POST'])
def recriar_senha():
    """
    Endpoint para definir a senha no primeiro acesso via token de convite.

    Espera receber no body:
    - `token`: str - token UUID recebido por e-mail
    - `password`: str - nova senha escolhida pelo usuário
    - `passwordConfirmation`: str - confirmação da nova senha

    Regras:
    - Token deve existir e estar marcado como used: false.
    - password e passwordConfirmation devem ser idênticos.
    - Senha deve ter no mínimo 8 caracteres, uma maiúscula, uma minúscula e um número.
    - Após uso bem-sucedido, o token é marcado como used: true e não pode ser reutilizado.

    Retorna:
    - `200 OK` com cookie JWT de sessão e dados do usuário.
    - `400 Bad Request` se as senhas não coincidirem ou não atenderem aos critérios.
    - `410 Gone` se o token for inválido ou já utilizado.

```json
    // 200 OK
    {
        "usuario": {
            "id": "id",
            "matricula": "matricula",
            "nome": "nome",
            "email": "email",
            "role": "role do usuario",
            "status": "status do usuario"
        },
        "redirect": "/painel/aluno"
    }
```
    """
    dados = request.get_json(silent=True) or {}

    token = dados.get('token')
    password = dados.get('password')
    password_confirmation = dados.get('passwordConfirmation')

    if not token or not password or not password_confirmation:
        return jsonify({
            "error": "Parâmetros 'token', 'password' e 'passwordConfirmation' são obrigatórios."
        }), 400

    if password != password_confirmation:
        return jsonify({"error": "As senhas não coincidem."}), 400

    erro_forca = _validar_forca_senha(password)
    if erro_forca:
        return jsonify({"error": erro_forca}), 400

    usuario_dict = definir_senha_primeiro_acesso(token, password)

    if not usuario_dict:
        return jsonify({
            "error": "Este link já foi utilizado ou é inválido.",
            "orientacao": "Utilize a opção 'Esqueci minha senha' para redefinir seu acesso."
        }), 410

    token_jwt = gerar_token(usuario_dict['id'], usuario_dict['role'])

    role_slug = usuario_dict['role'].split('.')[-1].lower()  # ex: "RoleEnum.ALUNO" → "aluno"

    response = make_response(jsonify({
        "usuario": usuario_dict,
        "redirect": f"/painel/{role_slug}"
    }), 200)

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