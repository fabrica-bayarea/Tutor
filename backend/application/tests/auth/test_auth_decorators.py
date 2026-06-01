"""
Testes unitários dos decoradores de autenticação/autorização.

Usam um app Flask mínimo apenas para fornecer contexto de requisição (`request`,
`g`, `jsonify`); as dependências de token são mockadas no namespace do módulo.
"""
import sys
from unittest.mock import MagicMock, patch

sys.modules.setdefault("chromadb", MagicMock())
sys.modules.setdefault("ollama", MagicMock())
sys.modules.setdefault("application.config.vector_database", MagicMock())

import pytest
from flask import Flask, g

import application.auth.auth_decorators as ad

flask_app = Flask(__name__)


def _eco():
    """View trivial protegida pelos decoradores."""
    return "ok"


# ---------------------------------------------------------------------------
# token_obrigatorio
# ---------------------------------------------------------------------------

def test_token_obrigatorio_sem_token_retorna_401():
    protegida = ad.token_obrigatorio(_eco)
    with flask_app.test_request_context():
        _, status = protegida()
    assert status == 401


def test_token_obrigatorio_token_na_denylist_retorna_401():
    protegida = ad.token_obrigatorio(_eco)
    with flask_app.test_request_context(headers={"Authorization": "Bearer x"}):
        with patch.object(ad, "token_invalido", return_value=True):
            _, status = protegida()
    assert status == 401


def test_token_obrigatorio_payload_invalido_retorna_401():
    protegida = ad.token_obrigatorio(_eco)
    with flask_app.test_request_context(headers={"Authorization": "Bearer x"}):
        with patch.object(ad, "token_invalido", return_value=False), \
             patch.object(ad, "validar_token", return_value=None):
            _, status = protegida()
    assert status == 401


def test_token_obrigatorio_usuario_bloqueado_retorna_401():
    # Cobre o encerramento de sessão de conta desativada (GAP-02-B).
    protegida = ad.token_obrigatorio(_eco)
    with flask_app.test_request_context(headers={"Authorization": "Bearer x"}):
        with patch.object(ad, "token_invalido", return_value=False), \
             patch.object(ad, "validar_token", return_value={"user_id": "u1", "role": "ALUNO"}), \
             patch.object(ad, "usuario_bloqueado", return_value=True):
            resp, status = protegida()
    assert status == 401


def test_token_obrigatorio_sucesso_chama_view_e_agenda_refresh():
    protegida = ad.token_obrigatorio(_eco)
    with flask_app.test_request_context(headers={"Authorization": "Bearer x"}):
        with patch.object(ad, "token_invalido", return_value=False), \
             patch.object(ad, "validar_token", return_value={"user_id": "u1", "role": "ADMIN"}), \
             patch.object(ad, "usuario_bloqueado", return_value=False), \
             patch.object(ad, "gerar_token", return_value="novo-token"):
            resultado = protegida()
            assert resultado == "ok"
            assert g.usuario_id == "u1"
            assert g.refresh_token == "novo-token"


def test_extrair_token_do_cookie():
    with flask_app.test_request_context():
        # sem header → cai no cookie
        with patch.object(ad.request, "cookies", {"token": "do-cookie"}):
            assert ad.extrair_token() == "do-cookie"


# ---------------------------------------------------------------------------
# Decoradores de papel
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("decorador,papel_ok", [
    (lambda f: ad.apenas_admins(f), "ADMIN"),
    (lambda f: ad.apenas_professores(f), "PROFESSOR"),
    (lambda f: ad.apenas_alunos(f), "ALUNO"),
])
def test_decoradores_de_papel_negam_sem_role(decorador, papel_ok):
    protegida = decorador(_eco)
    with flask_app.test_request_context():
        _, status = protegida()   # g.usuario_role ausente
    assert status == 403


@pytest.mark.parametrize("decorador,papel_ok", [
    (lambda f: ad.apenas_admins(f), "ADMIN"),
    (lambda f: ad.apenas_professores(f), "PROFESSOR"),
    (lambda f: ad.apenas_alunos(f), "ALUNO"),
])
def test_decoradores_de_papel_permitem_role_correto(decorador, papel_ok):
    protegida = decorador(_eco)
    with flask_app.test_request_context():
        g.usuario_role = papel_ok
        assert protegida() == "ok"
