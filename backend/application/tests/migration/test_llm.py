import sys
from unittest.mock import MagicMock, patch
import pytest

sys.modules["application.config.vector_database"] = MagicMock()
sys.modules["chromadb"] = MagicMock()
sys.modules["ollama"] = MagicMock()
sys.modules["application.socket.socket_instance"] = MagicMock()
sys.modules["application.socket.event_handler"] = MagicMock()

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_activate_model_apenas_um_ativo_por_vez(client):
    """Ao ativar um modelo, todos os outros devem ser desativados antes."""
    with patch("application.services.service_llm.LLM") as mock_llm, \
         patch("application.services.service_llm.db") as mock_db, \
         patch("application.services.service_llm.repository_ollama.model_installed", return_value=True):

        modelo_mock = MagicMock()
        modelo_mock.to_dict.return_value = {"model_id": "modelo-1", "status": "ativada"}
        mock_llm.query.filter_by.return_value.first.return_value = modelo_mock

        from application.services.service_llm import activateModel
        resultado = activateModel("modelo-1")

        # Garante que desativou todos antes de ativar
        mock_llm.query.filter_by.assert_any_call(status="ativada")
        mock_llm.query.filter_by.return_value.update.assert_called_once_with({"status": "desativada"})

        assert resultado["status"] == "ativada"
        mock_db.session.commit.assert_called_once()


def test_activate_model_inexistente_retorna_none(client):
    """Tentar ativar um modelo que não existe deve retornar None."""
    with patch("application.services.service_llm.LLM") as mock_llm:

        mock_llm.query.filter_by.return_value.first.return_value = None

        from application.services.service_llm import activateModel
        resultado = activateModel("modelo-inexistente")

        assert resultado is None
