"""
Testes das rotas RESTful de gestão de LLM (/llm).

Focam no contrato HTTP: status codes, formato da resposta e proteção de admin.
A regra de negócio do service é mockada (testada à parte em
tests/services/test_service_llm_pull.py), e a camada de autenticação é
substituída por um admin fixo para isolar o roteamento.
"""
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/test_route_llm.db")
os.environ.setdefault("SECRET_KEY", "test-secret")

sys.modules.setdefault("application.config.vector_database", MagicMock())
sys.modules.setdefault("chromadb", MagicMock())
sys.modules.setdefault("ollama", MagicMock())
sys.modules.setdefault("application.socket.socket_instance", MagicMock())
sys.modules.setdefault("application.socket.event_handler", MagicMock())

from app import app
from application.auth import auth_decorators
from application.services.service_llm import AddModelErro


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def admin_autenticado():
    """
    Faz toda requisição se comportar como um admin autenticado, substituindo as
    funções de auth usadas por `token_obrigatorio`/`apenas_admins`. Evita montar
    JWT/Redis reais e mantém o foco no contrato das rotas.
    """
    with patch.object(auth_decorators, "extrair_token", return_value="tok"), \
         patch.object(auth_decorators, "token_invalido", return_value=False), \
         patch.object(auth_decorators, "usuario_bloqueado", return_value=False), \
         patch.object(auth_decorators, "gerar_token", return_value="tok"), \
         patch.object(
             auth_decorators, "validar_token",
             return_value={"user_id": "admin-1", "role": "ADMIN"},
         ):
        yield


# --------------------------------------------------------------------------- #
# Proteção de admin
# --------------------------------------------------------------------------- #
def test_listar_modelos_nega_nao_admin(client):
    with patch.object(
        auth_decorators, "validar_token",
        return_value={"user_id": "u1", "role": "ALUNO"},
    ):
        resp = client.get("/llm")
    assert resp.status_code == 403


# --------------------------------------------------------------------------- #
# GET /llm e /llm/<id>
# --------------------------------------------------------------------------- #
def test_listar_modelos_retorna_200(client):
    with patch("application.routes.route_llm.getAllModels", return_value=[
        {"id": "1", "nome": "llama3", "status": "ativada"},
    ]):
        resp = client.get("/llm")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] == 1
    assert data["modelos"][0]["nome"] == "llama3"


def test_obter_modelo_por_id_404(client):
    with patch("application.routes.route_llm.getModelById", return_value=None):
        resp = client.get("/llm/abc")
    assert resp.status_code == 404


# --------------------------------------------------------------------------- #
# POST /llm
# --------------------------------------------------------------------------- #
def test_adicionar_modelo_201(client):
    with patch(
        "application.routes.route_llm.addModel",
        return_value=({"id": "1", "nome": "llama3", "status": "desativada"}, None),
    ):
        resp = client.post("/llm", json={"nome": "llama3"})
    assert resp.status_code == 201
    assert resp.get_json()["nome"] == "llama3"


def test_adicionar_modelo_sem_nome_400(client):
    with patch(
        "application.routes.route_llm.addModel",
        return_value=(None, AddModelErro.NOME_OBRIGATORIO),
    ):
        resp = client.post("/llm", json={})
    assert resp.status_code == 400


def test_adicionar_modelo_duplicado_409(client):
    with patch(
        "application.routes.route_llm.addModel",
        return_value=(None, AddModelErro.NOME_DUPLICADO),
    ):
        resp = client.post("/llm", json={"nome": "llama3"})
    assert resp.status_code == 409


def test_adicionar_modelo_inexistente_404(client):
    with patch(
        "application.routes.route_llm.addModel",
        return_value=(None, AddModelErro.MODELO_NAO_ENCONTRADO),
    ):
        resp = client.post("/llm", json={"nome": "nao-existe"})
    assert resp.status_code == 404


# --------------------------------------------------------------------------- #
# PUT / DELETE /llm/<id>
# --------------------------------------------------------------------------- #
def test_atualizar_modelo_200(client):
    with patch(
        "application.routes.route_llm.updateModel",
        return_value={"id": "1", "nome": "novo", "status": "desativada"},
    ):
        resp = client.put("/llm/1", json={"nome": "novo"})
    assert resp.status_code == 200
    assert resp.get_json()["nome"] == "novo"


def test_atualizar_modelo_404(client):
    with patch("application.routes.route_llm.updateModel", return_value=None):
        resp = client.put("/llm/1", json={"nome": "novo"})
    assert resp.status_code == 404


def test_deletar_modelo_200(client):
    with patch(
        "application.routes.route_llm.deleteModel",
        return_value={"id": "1", "nome": "llama3", "status": "desativada"},
    ):
        resp = client.delete("/llm/1")
    assert resp.status_code == 200


def test_deletar_modelo_404(client):
    with patch("application.routes.route_llm.deleteModel", return_value=None):
        resp = client.delete("/llm/1")
    assert resp.status_code == 404


# --------------------------------------------------------------------------- #
# POST/PUT /llm/activate/<id>
# --------------------------------------------------------------------------- #
def test_ativar_modelo_200(client):
    with patch(
        "application.routes.route_llm.activateModel",
        return_value={"id": "1", "nome": "llama3", "status": "ativada"},
    ):
        resp = client.post("/llm/activate/1")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ativada"


def test_ativar_modelo_aceita_put(client):
    with patch(
        "application.routes.route_llm.activateModel",
        return_value={"id": "1", "nome": "llama3", "status": "ativada"},
    ):
        resp = client.put("/llm/activate/1")
    assert resp.status_code == 200


def test_ativar_modelo_404(client):
    with patch("application.routes.route_llm.activateModel", return_value=None):
        resp = client.post("/llm/activate/1")
    assert resp.status_code == 404


def test_ativar_modelo_nao_instalado_409(client):
    from application.services.service_llm import ModeloNaoInstaladoError
    with patch(
        "application.routes.route_llm.activateModel",
        side_effect=ModeloNaoInstaladoError("fantasma"),
    ):
        resp = client.post("/llm/activate/1")
    assert resp.status_code == 409


# --------------------------------------------------------------------------- #
# GET /llm/pull-status/<id> (polling)
# --------------------------------------------------------------------------- #
def test_pull_status_retorna_progresso(client):
    with patch(
        "application.routes.route_llm.getPullProgress",
        return_value={"percent": 73, "status": "baixando"},
    ):
        resp = client.get("/llm/pull-status/1")
    assert resp.status_code == 200
    assert resp.get_json()["percent"] == 73


def test_pull_status_404(client):
    with patch("application.routes.route_llm.getPullProgress", return_value=None):
        resp = client.get("/llm/pull-status/1")
    assert resp.status_code == 404
