"""
Rotas para lidar com mensagens.

Para BUSCAR mensagens de um chat que JÁ EXISTE, usamos endpoints REST.
Para as demais operações CRUD, usamos eventos WebSockets.
"""
from flask import Blueprint, request, jsonify
from application.services.service_mensagem import *
from application.utils.validacoes import validar_chat, validar_aluno
from application.constants import LLM_UUID

mensagens_bp = Blueprint('mensagens', __name__)

# Endpoint para testar a criação de mensagens em ferramentas como Postman
# NÃO deve ser usado na aplicação real
@mensagens_bp.route('/criar', methods=['POST'])
def gerar_mensagem():
    """
    Endpoint para criar uma mensagem.

    Espera receber:
    - `chat_id`: uuid.UUID - o ID do chat
    - `sender_id`: uuid.UUID - o ID do remetente
    - `conteudo`: str - o conteúdo da mensagem
    
    Retorna a mensagem criada.
    ```json
    {
        "id": "id",
        "chat_id": "chat_id",
        "sender_id": "sender_id",
        "conteudo": "conteudo",
        "data_envio": "data_envio"
    }
    ```
    """
    chat_id = request.json['chat_id']
    sender_id = request.json['sender_id']
    conteudo = request.json['conteudo']
    
    if not chat_id or not sender_id or not conteudo:
        return jsonify({"error": "Parâmetros 'chat_id', 'sender_id' e 'conteudo' são obrigatórios"}), 400
    
    # Valida a existência do chat
    chat_existe = validar_chat(chat_id)
    if not chat_existe:
        return jsonify({"error": f"Chat com ID '{chat_id}' não encontrado"}), 404
    
    # Valida a existência do remetente
    aluno_existe = validar_aluno(sender_id)
    if not aluno_existe and sender_id != LLM_UUID:
        return jsonify({"error": f"Aluno com ID '{sender_id}' não encontrado"}), 404
    
    try:
        mensagem = criar_mensagem(chat_id, sender_id, conteudo)
        return jsonify(mensagem), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mensagens_bp.route('/chat/<string:chat_id>', methods=['GET'])
def obter_mensagens(chat_id: str):
    """
    Endpoint para buscar mensagens de um chat.

    Espera receber:
    - `chat_id`: uuid.UUID - o ID do chat
    
    Retorna as mensagens do chat.
    ```json
    [
        {
            "id": "id",
            "chat_id": "chat_id",
            "sender_id": "sender_id",
            "conteudo": "conteudo",
            "data_envio": "data_envio"
        }
    ]
    ```
    """
    chat_existe = validar_chat(chat_id)
    if not chat_existe:
        return jsonify({"error": f"Chat com ID '{chat_id}' não encontrado"}), 404
    
    try:
        mensagens = buscar_mensagens(chat_id)
        return jsonify(mensagens), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
