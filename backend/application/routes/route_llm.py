"""
Rotas para gerenciamento de modelos LLM.
"""
from flask import Blueprint, jsonify
from application.services.service_llm import getActiveModel

llm_bp = Blueprint('llm', __name__)


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