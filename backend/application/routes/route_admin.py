"""
Rotas para lidar com admin.
"""
from flask import Blueprint, jsonify, current_app, request, g
from application.auth.auth_decorators import token_obrigatorio, apenas_admins
from application.auth.token_denylist import bloquear_usuario, desbloquear_usuario
import uuid
from application.models.model_usuario import RoleEnum, Usuario
from application.models.model_materia import Materia
from application.models.model_turma import Turma
from application.services.service_usuario import (criar_usuario, buscar_aluno, desativar_aluno, alterar_aluno_por_id, reativar_aluno, buscar_alunos_por_filtro)
import secrets
from application.config.database import db
from datetime import datetime
from application.libs.email_sender import enviar_email_convite_async
from flask import make_response
from application.auth.jwt_handler import gerar_token, definir_cookie_sessao
from application.services.service_usuario import definir_senha_primeiro_acesso, _validar_forca_senha
from application.services.service_materia import getAllSubjects, createSubject, updateSubject, deleteSubject, buscar_materia_por_id

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/usuarios/all', methods=['GET'])
@token_obrigatorio
@apenas_admins
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
            turma =request.args.get('turma'),
            busca = request.args.get('busca')
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
@token_obrigatorio
@apenas_admins
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

    # Papel atribuído de forma atômica na criação (GAP-02-I). Default: ALUNO.
    role_str = (dados.get('role') or 'ALUNO').upper()
    if role_str not in ('ADMIN', 'PROFESSOR', 'ALUNO'):
        role_str = 'ALUNO'
    role_enum = RoleEnum[role_str]

    if not matricula or not nome or not email:
        return jsonify({"error": "Parâmetros 'matricula', 'nome' e 'email' são obrigatórios"}), 400

    if not email.endswith("@iesb.edu.br"):
        return jsonify({"error": "Email deve ser institucional (@iesb.edu.br)"}), 400

    # Checagem separada por campo, com as mensagens específicas do épico/Figma
    # (US-07-RV2/US-08-RV2). `campos` permite ao front marcar o campo certo.
    erros = {}
    if Usuario.query.filter(Usuario.matricula == matricula).first():
        erros["matricula"] = "Esta matrícula já está em uso por outro usuário."
    if Usuario.query.filter(Usuario.email == email).first():
        erros["email"] = "Este e-mail já está em uso por outro usuário."

    if erros:
        return jsonify({"error": " ".join(erros.values()), "campos": erros}), 409

    usuario_dict, token = criar_usuario(matricula, nome, email, via_google, role=role_enum)

    if not via_google and token:
        # Envio assíncrono (não bloqueia a resposta do cadastro) com timeout e
        # novas tentativas dentro da janela de 2 minutos exigida (US-03-RNF1).
        enviar_email_convite_async(email, nome, token)

    return jsonify(usuario_dict), 201


@admin_bp.route("/usuarios/delete/<uuid:id>", methods=['DELETE'])
@token_obrigatorio
@apenas_admins
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
    # GAP-02-C: o admin não pode desativar a própria conta.
    if str(g.usuario_id) == str(id):
        return jsonify({"error": "Você não pode desativar a própria conta."}), 403

    aluno = desativar_aluno(id)

    if not aluno:
        return jsonify({"error": "Usuario não encontrado"}), 404

    # GAP-02-B: encerra as sessões ativas do usuário desativado.
    bloquear_usuario(id)

    return jsonify({
        "Usuario:": aluno.nome,
        "Matricula:": aluno.matricula,
        "Data de desativação: ": datetime.now(),
        "mensagem": "Desativado com sucesso"
    }), 200



@admin_bp.route("/usuarios/<uuid:id>", methods=['GET'])
@token_obrigatorio
@apenas_admins
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
@token_obrigatorio
@apenas_admins
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

    # GAP-02-F: e-mail já usado por OUTRO usuário → 409 (em vez de IntegrityError/500).
    if Usuario.query.filter(Usuario.email == email, Usuario.id != id).first():
        return jsonify({
            "error": "Este e-mail já está em uso por outro usuário.",
            "campos": {"email": "Este e-mail já está em uso por outro usuário."},
        }), 409

    # GAP-02-E: matrícula é imutável após o cadastro — preserva a existente.
    aluno_novo = alterar_aluno_por_id(id, aluno_existente['matricula'], nome, email, status, role)

    return jsonify(aluno_novo), 200



@admin_bp.route("/usuarios/<uuid:id>/reativar", methods=['PATCH'])
@token_obrigatorio
@apenas_admins
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

    # Reabilita as sessões do usuário reativado (contrapartida do GAP-02-B).
    desbloquear_usuario(id)

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

    definir_cookie_sessao(response, token_jwt)

    return response

"""

MATERIA

"""
@admin_bp.route('/materia', methods=['GET'])
@token_obrigatorio
@apenas_admins
def lista_materias():
    
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', type=int)

    materia = getAllSubjects(nome = request.args.get('nome'), codigo = request.args.get('codigo'))

    if limit:
        pagination = materia.paginate(page=page, per_page=limit, error_out=False)

        return jsonify({
            "success": True,
            "Materias": [m.to_dict() for m in pagination.items],
            "pagination": {
                "page": pagination.page,
                "pages": pagination.pages,
                "total": pagination.total
                }
        }), 200
    
    materia = materia.all()

    return jsonify({
        "success": True,
        "Materias": [m.to_dict() for m in materia],
        "total": len(materia)
        }), 200



@admin_bp.route('/materia', methods=['POST'])
@token_obrigatorio
@apenas_admins
def gerar_materia():

    dados = request.get_json(silent=True) or {}

    codigo = dados.get('codigo')
    nome = dados.get('nome')


    if not codigo or not nome:
        return jsonify({"error": "Parâmetros 'codigo' e 'nome' são obrigatórios"}), 400


    existente = Materia.query.filter(
        (Materia.codigo == codigo)
    ).first()

    if existente:
        return jsonify({"Error": "Já existe uma matéria com este código."}), 409

    materia_dict = createSubject(nome=nome, codigo=codigo)


    return jsonify(materia_dict), 201


@admin_bp.route('/materia/<uuid:id>', methods=['PUT'])
@token_obrigatorio
@apenas_admins
def atualizar_materia(id):
    nome = request.json.get('nome')
    codigo = request.json.get('codigo')
    status = request.json.get('status')


    if not codigo or not nome:
        return jsonify({"error": "Parâmetros 'nome', 'codigo' e 'status' são obrigatórios"}), 400

    
    if status not in ["ATIVO", "INATIVO"]:
        return jsonify({"error": "Status deve ser ATIVO ou INATIVO"}), 400

    materia_existente = buscar_materia_por_id(id)

    if not materia_existente:
        return jsonify({"Error": "Materia não econtrada"}), 404

    # G5: o código é imutável após o cadastro — preserva o existente, ignorando
    # qualquer valor enviado no corpo (bloqueio já existia só no frontend).
    materia_nova = updateSubject(id, nome, materia_existente['codigo'], status)

    return jsonify(materia_nova), 200


@admin_bp.route('/materia/<uuid:id>', methods=['DELETE'])
@token_obrigatorio
@apenas_admins
def deletar_materias(id):

    materia, erro = deleteSubject(id)

    if erro:
        if 'materia_nao_encontrada' in erro:
            return jsonify({"error": "Materia não encontrada"}), 404

        if 'materia_vinculada_turma_ativa' in erro:
            return jsonify({
                "error": "Matéria vinculada a turma ativa"
            }), 409

        if 'materia_nao_pode_ser_desativada' in erro:
            return jsonify({
                "error": "Matéria não pode ser desativada"
            }), 409

    return jsonify({
        "data_desativacao": datetime.now(),
        "mensagem": "Desativado com sucesso"
    }), 200