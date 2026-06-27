"""
Rotas  para lidar com mensagens.

Para BUSCAR mensagens de um chat que JÁ EXISTE, usamos endpoints REST.
Para as demais operações CRUD, usamos eventos WebSockets.
"""
from flask import Blueprint, jsonify
from application.services.service_mensagem import *
from application.utils.validacoes import validar_chat

mensagens_bp = Blueprint('mensagens', __name__)

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
            "sender_type": "user"|"llm"
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
