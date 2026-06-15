"""
Rotas para gerenciamento de modelos de IA (LLM).

Expõe um CRUD RESTful sob `/llm`, a ativação exclusiva de um modelo e a consulta
de progresso do download (pull) por polling. As rotas de gestão são restritas a
administradores; `GET /llm/active`, consumida pelo fluxo de chat, permanece
pública.

A regra de negócio mora em `services/service_llm.py`; aqui só validamos a
entrada, delegamos e traduzimos o resultado em resposta HTTP.
"""
from flask import Blueprint, jsonify, request

from application.auth.auth_decorators import token_obrigatorio, apenas_admins
from application.services.service_llm import (
    AddModelErro,
    getActiveModel,
    getAllModels,
    getModelById,
    addModel,
    updateModel,
    deleteModel,
    activateModel,
    getPullProgress,
)

llm_bp = Blueprint('llm', __name__)

# Despacho de cada falha de `addModel` para (mensagem, status HTTP). Um mapa em
# vez de uma cadeia de `if` mantém a rota plana e centraliza o contrato de erro.
_RESPOSTA_ADD_MODEL: dict[AddModelErro, tuple[str, int]] = {
    AddModelErro.NOME_OBRIGATORIO: ("O campo 'nome' é obrigatório", 400),
    AddModelErro.NOME_DUPLICADO: ("Já existe um modelo com esse nome", 409),
    AddModelErro.MODELO_NAO_ENCONTRADO: ("Modelo não encontrado no Ollama", 404),
    AddModelErro.OLLAMA_INDISPONIVEL: ("Servidor Ollama indisponível", 503),
}


@llm_bp.route('/llm/active', methods=['GET'])
def obter_modelo_ativo():
    """
    Endpoint para consultar o modelo de IA atualmente ativo.

    Retorna o nome do modelo ativo em formato JSON:
```json
    { "activeModel": "nome_modelo" }
```

    Se não houver nenhum modelo ativo, retorna HTTP 404:
```json
    { "error": "Nenhum modelo ativo encontrado" }
```
    """
    nome = getActiveModel()

    if nome is None:
        return jsonify({"error": "Nenhum modelo ativo encontrado"}), 404

    return jsonify({"activeModel": nome}), 200


@llm_bp.route('/llm', methods=['GET'])
@token_obrigatorio
@apenas_admins
def listar_modelos():
    """
    Endpoint para listar todos os modelos de IA cadastrados.

    Retorna HTTP 200 com a lista de modelos:
```json
    { "modelos": [ { "id": "...", "nome": "...", "status": "..." } ], "total": 1 }
```
    """
    modelos = getAllModels()
    return jsonify({"modelos": modelos, "total": len(modelos)}), 200


@llm_bp.route('/llm/<string:model_id>', methods=['GET'])
@token_obrigatorio
@apenas_admins
def obter_modelo_por_id(model_id: str):
    """
    Endpoint para buscar um modelo de IA pelo seu ID.

    Espera receber:
    - `model_id`: str - o ID do modelo (na URL).

    Retorna HTTP 200 com o modelo, ou 404 se ele não existir.
    """
    modelo = getModelById(model_id)

    if modelo is None:
        return jsonify({"error": "Modelo não encontrado"}), 404

    return jsonify(modelo), 200


@llm_bp.route('/llm', methods=['POST'])
@token_obrigatorio
@apenas_admins
def adicionar_modelo():
    """
    Endpoint para adicionar um novo modelo e iniciar o download (pull) no Ollama.

    Espera receber no corpo:
    - `nome`: str - o nome do modelo no Ollama (ex.: "llama3").

    Fluxo: cria o registro, valida a existência no Ollama e dispara o pull em
    segundo plano. O progresso é acompanhado por `GET /llm/pull-status/<id>`.

    Respostas:
    - 201: modelo criado e pull iniciado.
    - 400: `nome` ausente.
    - 404: modelo inexistente no Ollama (o registro criado é desfeito).
    - 409: já existe um modelo com esse nome.
    - 503: servidor Ollama indisponível.
    """
    dados = request.get_json(silent=True) or {}

    modelo, erro = addModel(dados)

    if erro is not None:
        mensagem, status = _RESPOSTA_ADD_MODEL[erro]
        return jsonify({"error": mensagem}), status

    return jsonify(modelo), 201


@llm_bp.route('/llm/<string:model_id>', methods=['PUT'])
@token_obrigatorio
@apenas_admins
def atualizar_modelo(model_id: str):
    """
    Endpoint para atualizar um modelo (apenas o `nome`).

    Espera receber:
    - `model_id`: str - o ID do modelo (na URL).
    - `nome`: str - o novo nome (no corpo).

    Retorna HTTP 200 com o modelo atualizado, ou 404 se ele não existir.
    """
    dados = request.get_json(silent=True) or {}

    modelo = updateModel(model_id, dados)

    if modelo is None:
        return jsonify({"error": "Modelo não encontrado"}), 404

    return jsonify(modelo), 200


@llm_bp.route('/llm/<string:model_id>', methods=['DELETE'])
@token_obrigatorio
@apenas_admins
def deletar_modelo(model_id: str):
    """
    Endpoint para remover um modelo de IA.

    Espera receber:
    - `model_id`: str - o ID do modelo (na URL).

    Retorna HTTP 200 ao remover, ou 404 se o modelo não existir.
    """
    modelo = deleteModel(model_id)

    if modelo is None:
        return jsonify({"error": "Modelo não encontrado"}), 404

    return jsonify({"mensagem": "Modelo removido com sucesso"}), 200


@llm_bp.route('/llm/activate/<string:model_id>', methods=['POST', 'PUT'])
@token_obrigatorio
@apenas_admins
def ativar_modelo_por_id(model_id: str):
    """
    Endpoint para ativar um modelo, desativando todos os demais.

    Espera receber:
    - `model_id`: str - o ID do modelo a ativar (na URL).

    Retorna HTTP 200 com o modelo ativado, ou 404 se ele não existir.
    """
    modelo = activateModel(model_id)

    if modelo is None:
        return jsonify({"error": "Modelo não encontrado"}), 404

    return jsonify(modelo), 200


@llm_bp.route('/llm/pull-status/<string:model_id>', methods=['GET'])
@token_obrigatorio
@apenas_admins
def status_do_pull(model_id: str):
    """
    Endpoint de polling para acompanhar o progresso do download (pull) de um
    modelo (0–100%).

    Espera receber:
    - `model_id`: str - o ID do modelo (na URL).

    Retorna HTTP 200 com o progresso:
```json
    { "percent": 73, "status": "baixando" }
```
    ou 404 se o modelo não existir.
    """
    progresso = getPullProgress(model_id)

    if progresso is None:
        return jsonify({"error": "Modelo não encontrado"}), 404

    return jsonify(progresso), 200
