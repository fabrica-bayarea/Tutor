"""
Testes de rota para autenticação (set-password e forgot-password).

Tudo mockado (sem banco): valida os fluxos de criação/redefinição de senha e de
recuperação por e-mail, incluindo o caminho de sucesso que emite o cookie de sessão.
"""
import sys
from unittest.mock import MagicMock, patch
import pytest

sys.modules.setdefault("application.config.vector_database", MagicMock())
sys.modules.setdefault("chromadb", MagicMock())
sys.modules.setdefault("ollama", MagicMock())
sys.modules.setdefault("application.socket.socket_instance", MagicMock())
sys.modules.setdefault("application.socket.event_handler", MagicMock())

from app import app
from application.models.model_usuario import StatusEnum


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# POST /auth/invite/set-password
# ---------------------------------------------------------------------------

def test_set_password_parametros_ausentes(client):
    resp = client.post("/auth/invite/set-password", json={})
    assert resp.status_code == 400


def test_set_password_confirmacao_divergente(client):
    resp = client.post("/auth/invite/set-password", json={
        "token": "tok", "senha": "Senha123", "confirmacao": "Outra123",
    })
    assert resp.status_code == 422


@patch("application.routes.route_auth.validar_token_convite", return_value=(None, "utilizado_ou_inexistente"))
def test_set_password_token_invalido(_mock_validar, client):
    resp = client.post("/auth/invite/set-password", json={"token": "tok", "senha": "Senha123"})
    assert resp.status_code == 410


@patch("application.routes.route_auth.definir_senha_primeiro_acesso", return_value=None)
@patch("application.routes.route_auth.validar_token_convite", return_value=(None, "valido"))
def test_set_password_senha_fraca(_mock_validar, _mock_definir, client):
    resp = client.post("/auth/invite/set-password", json={"token": "tok", "senha": "fraca"})
    assert resp.status_code == 422


@patch("application.routes.route_auth.definir_cookie_sessao")
@patch("application.routes.route_auth.gerar_token", return_value="jwt-fake")
@patch("application.routes.route_auth.definir_senha_primeiro_acesso",
       return_value={"id": "u1", "role": "ALUNO"})
@patch("application.routes.route_auth.validar_token_convite", return_value=(None, "valido"))
def test_set_password_sucesso_emite_sessao(_mock_validar, _mock_definir, mock_gerar, mock_cookie, client):
    resp = client.post("/auth/invite/set-password", json={
        "token": "tok", "senha": "Senha123", "confirmacao": "Senha123",
    })
    assert resp.status_code == 200
    assert resp.get_json()["usuario"]["id"] == "u1"
    mock_gerar.assert_called_once_with("u1", "ALUNO")
    mock_cookie.assert_called_once()


# ---------------------------------------------------------------------------
# POST /auth/forgot-password
# ---------------------------------------------------------------------------

def test_forgot_password_email_ausente(client):
    resp = client.post("/auth/forgot-password", json={})
    assert resp.status_code == 400


@patch("application.routes.route_auth.enviar_email_recuperacao_senha")
@patch("application.routes.route_auth.db")
@patch("application.routes.route_auth.TokenConvite")
@patch("application.routes.route_auth.Usuario")
def test_forgot_password_usuario_ativo_gera_token_e_envia(mock_usuario, mock_token, mock_db, mock_email, client):
    usuario = MagicMock(id="u1", email="a@iesb.edu.br", nome="Ana", status=StatusEnum.ATIVO)
    mock_usuario.query.filter_by.return_value.first.return_value = usuario

    resp = client.post("/auth/forgot-password", json={"email": "a@iesb.edu.br"})

    assert resp.status_code == 200
    mock_email.assert_called_once()
    assert mock_db.session.commit.called


@patch("application.routes.route_auth.Usuario")
def test_forgot_password_email_desconhecido_responde_generico(mock_usuario, client):
    # não revela se o e-mail existe — resposta genérica 200
    mock_usuario.query.filter_by.return_value.first.return_value = None
    resp = client.post("/auth/forgot-password", json={"email": "naoexiste@iesb.edu.br"})
    assert resp.status_code == 200
