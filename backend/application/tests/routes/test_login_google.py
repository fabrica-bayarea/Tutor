import sys
from unittest.mock import MagicMock, patch
import pytest

sys.modules["application.config.vector_database"] = MagicMock()
sys.modules["chromadb"] = MagicMock()
sys.modules["ollama"] = MagicMock()
sys.modules["application.socket.socket_instance"] = MagicMock()
sys.modules["application.socket.event_handler"] = MagicMock()

from app import app

DOMINIO_VALIDO = "@iesb.edu.br"
GOOGLE_TOKEN_VALIDO = "token-google-simulado"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_login_google_sem_token(client):
    response = client.post("/alunos/login/google", json={})
    assert response.status_code == 400
    assert "Token não enviado" in response.get_json()["error"]


def test_login_google_token_invalido(client):
    with patch("application.routes.route_usuarios.id_token.verify_oauth2_token") as mock_verify:
        mock_verify.side_effect = ValueError("Token inválido")

        response = client.post("/alunos/login/google", json={"token": "token-invalido"})

        assert response.status_code == 401
        assert "Token inválido" in response.get_json()["error"]


def test_login_google_dominio_invalido(client):
    with patch("application.routes.route_usuarios.id_token.verify_oauth2_token") as mock_verify:
        mock_verify.return_value = {
            "email": "usuario@gmail.com",
            "name": "Usuário Externo",
            "sub": "123456789"
        }

        response = client.post("/alunos/login/google", json={"token": GOOGLE_TOKEN_VALIDO})

        assert response.status_code == 403
        data = response.get_json()
        assert DOMINIO_VALIDO in data["error"]


def test_login_google_usuario_nao_cadastrado(client):
    with patch("application.routes.route_usuarios.id_token.verify_oauth2_token") as mock_verify, \
         patch("application.routes.route_usuarios.Usuario") as mock_usuario:

        mock_verify.return_value = {
            "email": "naoexiste@iesb.edu.br",
            "name": "Não Existe",
            "sub": "987654321"
        }
        mock_usuario.query.filter_by.return_value.first.return_value = None

        response = client.post("/alunos/login/google", json={"token": GOOGLE_TOKEN_VALIDO})

        assert response.status_code == 404
        data = response.get_json()
        # Mensagem alinhada ao épico/Figma (US-02-RV1).
        assert "não está vinculada" in data["error"].lower()


def test_login_google_sucesso(client):
    with patch("application.routes.route_usuarios.id_token.verify_oauth2_token") as mock_verify, \
         patch("application.routes.route_usuarios.Usuario") as mock_usuario, \
         patch("application.routes.route_usuarios.gerar_token") as mock_gerar_token:

        mock_verify.return_value = {
            "email": "aluno@iesb.edu.br",
            "name": "Aluno Teste",
            "sub": "111222333"
        }

        aluno_mock = MagicMock()
        aluno_mock.id = "uuid-fake-123"
        aluno_mock.role.value = "3"
        aluno_mock.status.name = "ATIVO"  # usuário ativo: necessário p/ passar na checagem de status
        aluno_mock.to_dict.return_value = {
            "id": "uuid-fake-123",
            "matricula": "20260001",
            "nome": "Aluno Teste",
            "email": "aluno@iesb.edu.br",
            "role": "3"
        }
        mock_usuario.query.filter_by.return_value.first.return_value = aluno_mock
        mock_gerar_token.return_value = "jwt-token-fake"

        response = client.post("/alunos/login/google", json={"token": GOOGLE_TOKEN_VALIDO})

        assert response.status_code == 200
        data = response.get_json()
        assert "aluno" in data
        assert data["aluno"]["email"] == "aluno@iesb.edu.br"
        assert "token" in response.headers.get("Set-Cookie", "")


def test_login_google_nao_cria_usuario(client):
    with patch("application.routes.route_usuarios.id_token.verify_oauth2_token") as mock_verify, \
         patch("application.routes.route_usuarios.Usuario") as mock_usuario, \
         patch("application.routes.route_usuarios.db") as mock_db:

        mock_verify.return_value = {
            "email": "novo@iesb.edu.br",
            "name": "Novo Usuário",
            "sub": "444555666"
        }
        mock_usuario.query.filter_by.return_value.first.return_value = None

        response = client.post("/alunos/login/google", json={"token": GOOGLE_TOKEN_VALIDO})

        mock_db.session.add.assert_not_called()
        mock_db.session.commit.assert_not_called()
        assert response.status_code == 404