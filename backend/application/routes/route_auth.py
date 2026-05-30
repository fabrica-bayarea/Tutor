"""
Rotas de autenticação — primeiro acesso e redefinição de senha.
"""
import uuid
from flask import Blueprint, jsonify, request, current_app
from application.config.database import db
from application.models.model_usuario import Usuario, RoleEnum
from application.models.model_token_convite import TokenConvite
from application.services.service_usuario import (validar_token_convite, definir_senha_primeiro_acesso)
from application.libs.email_sender import enviar_email_recuperacao_senha
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
    - `confirmacao`: str — repetição da nova senha para confirmação

    Regras:
    - Token precisa existir e não ter sido utilizado (campo `used=False`).
    - `senha` e `confirmacao` devem ser idênticas.
    - Senha validada pelo `_validar_forca_senha` do próprio service:
      8+ chars, maiúscula, minúscula e número.
    - Após salvar o hash da senha, `TokenConvite.used` é marcado como True.

    Retorna:
    - `200 OK` com dados básicos do usuário após sucesso.
    - `400 Bad Request` se parâmetros ausentes.
    - `410 Gone` se token inválido ou já utilizado.
    - `422 Unprocessable Entity` se as senhas não conferem ou não atendem aos requisitos.
 
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
    confirmacao = data.get('confirmacao', '')

    if not token or not senha:
        return jsonify({"error": "Parâmetros 'token' e 'senha' são obrigatórios"}), 400

    if senha != confirmacao:
        return jsonify({"error": "As senhas não conferem. Por favor, digite novamente."}), 422

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


@auth_bp.route('/forgot-password', methods=['POST'])
def recuperar_senha():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip()

    if not email:
        return jsonify({"error": "Email é obrigatório"}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and usuario.status == RoleEnum.ATIVO:
        TokenConvite.query.filter_by(usuario_id=usuario.id, used=False).update({'used': True})
        db.session.commit()

        token_str = str(uuid.uuid4())
        novo_token = TokenConvite(token=token_str, usuario_id=usuario.id)
        db.session.add(novo_token)
        db.session.commit()

        try:
            enviar_email_recuperacao_senha(usuario.email, usuario.nome, token_str)
        except Exception as e:
            current_app.logger.error(f"Erro ao enviar e-mail de recuperação para {email}: {e}")

    return jsonify({"mensagem": "Se o e-mail estiver cadastrado, você receberá um link em instantes."}), 200
