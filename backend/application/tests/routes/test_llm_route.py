import sys
from unittest.mock import MagicMock
import uuid

sys.modules["application.config.vector_database"] = MagicMock()
sys.modules["chromadb"] = MagicMock()
sys.modules["ollama"] = MagicMock()
sys.modules["application.socket.socketio"] = MagicMock()

from app import app
from application.config.database import db
from application.models.model_llm import LLM


def _limpar_llms():
    LLM.query.delete()
    db.session.commit()


def test_rota_modelo_ativo_retorna_nome():
    """
    /llm/active deve retornar 200 e { "activeModel": "<nome>" }
    quando há um modelo com status='ativada' no banco.
    """
    with app.app_context():
        _limpar_llms()

        modelo = LLM(id=str(uuid.uuid4()), nome="llama3", status="ativada")
        db.session.add(modelo)
        db.session.commit()

        client = app.test_client()
        response = client.get("/llm/active")

        assert response.status_code == 200
        data = response.get_json()
        assert "activeModel" in data
        assert data["activeModel"] == "llama3"

        _limpar_llms()


def test_rota_modelo_ativo_retorna_404_sem_modelo():
    """
    /llm/active deve retornar 404 e { "error": "..." }
    quando não há nenhum modelo com status='ativada'.
    """
    with app.app_context():
        _limpar_llms()

        client = app.test_client()
        response = client.get("/llm/active")

        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Nenhum modelo ativo encontrado"


def test_rota_nao_depende_de_materia():
    """
    A rota /llm/active não deve depender de nenhuma matéria.
    Deve retornar o modelo ativo mesmo sem nenhuma matéria no banco.
    """
    with app.app_context():
        _limpar_llms()

        modelo = LLM(id=str(uuid.uuid4()), nome="mistral", status="ativada")
        db.session.add(modelo)
        db.session.commit()

        client = app.test_client()
        response = client.get("/llm/active")

        assert response.status_code == 200
        assert response.get_json()["activeModel"] == "mistral"

        _limpar_llms()


if __name__ == "__main__":
    test_rota_modelo_ativo_retorna_nome()
    test_rota_modelo_ativo_retorna_404_sem_modelo()
    test_rota_nao_depende_de_materia()
    print("Todos os testes de rota passaram.")