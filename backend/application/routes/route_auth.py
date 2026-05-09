"""
Rotas de autenticação — primeiro acesso e redefinição de senha.
"""
from flask import Blueprint, jsonify
from application.services.service_usuario import validar_token_convite
from flask import request, jsonify
from application.services.service_usuario import (validar_token_convite,definir_senha_primeiro_acesso, )
import re

REGEX_SENHA = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$')
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/invite/validate/<string:token>', methods=['GET'])
def validar_convite(token):
    """
    Endpoint para validar o token de convite antes de exibir o formulário
    de criação de senha no primeiro acesso.

    Espera receber:
    - `token`: str - token UUID enviado via URL

    Retorna:
    - `200 OK` com dados básicos do usuário se o token existir e não tiver sido utilizado.
    - `410 Gone` com orientação para "Esqueci minha senha" se o token já foi utilizado
      ou não existir.

```json
    // 200 OK
    {
        "nome": "nome do usuário",
        "email": "email do usuário"
    }

    // 410 Gone
    {
        "error": "Este link já foi utilizado ou é inválido.",
        "orientacao": "Utilize a opção 'Esqueci minha senha' para redefinir seu acesso."
    }
```
    """
    usuario_dados, status = validar_token_convite(token)

    if status == 'utilizado_ou_inexistente':
        return jsonify({
            "error": "Este link já foi utilizado ou é inválido.",
            "orientacao": "Utilize a opção 'Esqueci minha senha' para redefinir seu acesso."
        }), 410

    return jsonify(usuario_dados), 200
    
@auth_bp.route('/invite/set-password', methods=['POST'])
def definir_senha():
    """
    Endpoint para criar a senha no primeiro acesso ou redefinição.
 
    Espera receber (JSON):
    - `token`: str — token UUID do convite
    - `senha`: str — nova senha escolhida pelo usuário
 
    Regras:
    - Token precisa existir e não ter sido utilizado (campo `used=False`).
    - Senha validada pelo `_validar_forca_senha` do próprio service:
      8+ chars, maiúscula, minúscula e número.
    - Após salvar o hash da senha, `TokenConvite.used` é marcado como True.
 
    Retorna:
    - `200 OK` com dados básicos do usuário após sucesso.
    - `400 Bad Request` se parâmetros ausentes.
    - `410 Gone` se token inválido ou já utilizado.
    - `422 Unprocessable Entity` se a senha não atende aos requisitos.
 
```json
    // 200 OK
    { "mensagem": "Senha criada com sucesso." }
 
    // 400 Bad Request
    { "error": "Parâmetros 'token' e 'senha' são obrigatórios" }
 
    // 410 Gone
    {
        "error": "Este link já foi utilizado ou é inválido.",
        "orientacao": "Utilize a opção 'Esqueci minha senha' para redefinir seu acesso."
    }
 
    // 422 Unprocessable Entity
    {
        "error": "A senha não atende aos requisitos mínimos.",
        "requisitos": "Mínimo 8 caracteres, uma letra maiúscula, uma minúscula e um número."
    }
```
    """
    data = request.get_json(silent=True) or {}
    token = data.get('token', '').strip()
    senha = data.get('senha', '')
 
    if not token or not senha:
        return jsonify({"error": "Parâmetros 'token' e 'senha' são obrigatórios"}), 400
 
    _, status_token = validar_token_convite(token)
    if status_token == 'utilizado_ou_inexistente':
        return jsonify({
            "error": "Este link já foi utilizado ou é inválido.",
            "orientacao": "Utilize a opção 'Esqueci minha senha' para redefinir seu acesso."
        }), 410
 
    usuario = definir_senha_primeiro_acesso(token, senha)
 
    if usuario is None:
        return jsonify({
            "error": "A senha não atende aos requisitos mínimos.",
            "requisitos": "Mínimo 8 caracteres, uma letra maiúscula, uma minúscula e um número."
        }), 422
 
    return jsonify({"mensagem": "Senha criada com sucesso."}), 200
 