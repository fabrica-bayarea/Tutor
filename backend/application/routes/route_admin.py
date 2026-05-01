"""
Rotas para lidar com admin.
"""
from flask import Blueprint, jsonify, current_app, request
from application.auth.auth_decorators import token_obrigatorio
import uuid
from application.models.model_usuario import RoleEnum, Usuario
from application.models.model_turma import Turma
from application.services.service_usuario import criar_aluno, buscar_aluno
import secrets

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/usuarios/all', methods=['GET'])
def listar_todos_usuarios():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', type=int)

        filtros = {
            Usuario.nome: request.args.get('nome'),
            Usuario.matricula: request.args.get('matricula'),
            Usuario.role: request.args.get('role'),
            Usuario.status: request.args.get('status'),
            Turma.codigo: request.args.get('turma')
        }

        query = Usuario.query

        for campo, valor in filtros.items():
            if valor:
                if campo in [Usuario.nome, Usuario.matricula, Turma.codigo]:
                    query = query.filter(campo.ilike(f"%{valor}%"))
                else:
                    query = query.filter(campo == valor)

        query = query.order_by(Usuario.nome.asc())

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
