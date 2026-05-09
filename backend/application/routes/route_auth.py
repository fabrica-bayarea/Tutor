"""
Rotas de autenticação — primeiro acesso e redefinição de senha.
"""
from flask import Blueprint, jsonify
from application.services.service_usuario import validar_token_convite

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