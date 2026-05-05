"""
Rotas para lidar com admin.
"""
from flask import Blueprint, jsonify, current_app, request
from application.auth.auth_decorators import token_obrigatorio
import uuid
from application.models.model_usuario import RoleEnum, Usuario
from application.models.model_turma import Turma
from application.services.service_usuario import criar_aluno, buscar_aluno, desativar_aluno, alterar_aluno_por_id, reativar_aluno, buscar_alunos_por_filtro
import secrets
from application.config.database import db
from datetime import datetime

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


    
@admin_bp.route('usuarios/criar', methods=['POST'])
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

    if not email.endswith("@iesb.edu.br"):
        return jsonify({"error": "Email deve ser institucional (@iesb.edu.br)"}), 400
    
    if not matricula or not nome or not email:
        return jsonify({"error": "Parâmetros 'matricula', 'nome', 'email' e 'senha' são obrigatórios"}), 400
    
    existente = Usuario.query.filter(
        (Usuario.matricula == matricula) | (Usuario.email == email)
    ).first()

    if existente:
        return jsonify({"error": "Email ou matrícula já cadastrados."}), 409
    
    senha = secrets.token_hex(4)

    # Verifica se já existe um aluno com alguns dados que devem ser únicos
    aluno_existe = buscar_aluno(matricula=matricula, email=email)
    if aluno_existe:
        print('ca')
        return jsonify({"error": "Aluno com essa matrícula ou email já existe"}), 409
    
    # Cria o aluno
    aluno = criar_aluno(matricula, nome, email, senha)
    return jsonify(aluno), 201


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

