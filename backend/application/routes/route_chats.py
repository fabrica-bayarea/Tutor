"""
Rotas para lidar com chats.

Para CRIAR um chat, usamos eventos WebSockets.
Para as demais operações CRUD, usamos endpoints REST.
"""
from flask import Blueprint, request, jsonify, g
from application.auth.auth_decorators import token_obrigatorio, apenas_alunos
from application.services.service_chat import buscar_chats, buscar_chat, atualizar_chat, deletar_chat

chats_bp = Blueprint('chats', __name__)

@chats_bp.route('/aluno/<aluno_id>', methods=['GET'])
@token_obrigatorio
@apenas_alunos
def obter_chats(aluno_id):
    try:
        if aluno_id != g.usuario_id:
            return jsonify({'error': 'Operação não autorizada'}), 403
        
        chats = buscar_chats(aluno_id)
        return jsonify(chats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chats_bp.route('/chat/<string:chat_id>', methods=['PATCH'])
@token_obrigatorio
@apenas_alunos
def update_chat(chat_id: str):
    # Verifica se os dados necessários estão presentes
    novo_nome = request.json.get('nome')
    if not novo_nome:
        return jsonify({'error': 'Parâmetro "nome" é obrigatório'}), 400
    
    try:
        chat = buscar_chat(chat_id)
        if not chat:
            return jsonify({'error': 'Chat não encontrado'}), 404
        
        if chat['aluno_id'] != g.usuario_id:
            return jsonify({'error': 'Operação não autorizada'}), 403
        
        chat_atualizado = atualizar_chat(chat_id, novo_nome)
        return jsonify(chat_atualizado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chats_bp.route('/chat/<string:chat_id>', methods=['DELETE'])
@token_obrigatorio
@apenas_alunos
def delete_chat(chat_id: str):
    try:
        chat = buscar_chat(chat_id)
        if not chat:
            return jsonify({'error': 'Chat não encontrado'}), 404
        
        if chat['aluno_id'] != g.usuario_id:
            return jsonify({'error': 'Operação não autorizada'}), 403
        
        deletado = deletar_chat(chat_id)
        return jsonify(deletado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
