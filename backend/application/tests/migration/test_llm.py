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


def test_ativar_modelo_apenas_um_ativo_por_vez(client):
    """Ao ativar um modelo, todos os outros devem ser desativados antes."""
    with patch("application.services.service_llm.LLM") as mock_llm, \
         patch("application.services.service_llm.db") as mock_db:

        modelo_mock = MagicMock()
        modelo_mock.to_dict.return_value = {"model_id": "modelo-1", "status": "ativada"}
        mock_llm.query.filter_by.return_value.first.return_value = modelo_mock

        from application.services.service_llm import ativar_modelo
        resultado = ativar_modelo("modelo-1")

        # Garante que desativou todos antes de ativar
        mock_llm.query.filter_by.assert_any_call(status="ativada")
        mock_llm.query.filter_by.return_value.update.assert_called_once_with({"status": "desativada"})

        assert resultado["status"] == "ativada"
        mock_db.session.commit.assert_called_once()


def test_ativar_modelo_inexistente_retorna_none(client):
    """Tentar ativar um modelo que não existe deve retornar None."""
    with patch("application.services.service_llm.LLM") as mock_llm:

        mock_llm.query.filter_by.return_value.first.return_value = None

        from application.services.service_llm import ativar_modelo
        resultado = ativar_modelo("modelo-inexistente")

        assert resultado is None


def test_desativar_modelo_existente(client):
    """Desativar um modelo existente deve alterar status para 'desativada'."""
    with patch("application.services.service_llm.LLM") as mock_llm, \
         patch("application.services.service_llm.db") as mock_db:

        modelo_mock = MagicMock()
        modelo_mock.to_dict.return_value = {"model_id": "modelo-1", "status": "desativada"}
        mock_llm.query.filter_by.return_value.first.return_value = modelo_mock

        from application.services.service_llm import desativar_modelo
        resultado = desativar_modelo("modelo-1")

        assert resultado["status"] == "desativada"
        mock_db.session.commit.assert_called_once()


def test_desativar_modelo_inexistente_retorna_none(client):
    """Tentar desativar um modelo que não existe deve retornar None."""
    with patch("application.services.service_llm.LLM") as mock_llm:

        mock_llm.query.filter_by.return_value.first.return_value = None

        from application.services.service_llm import desativar_modelo
        resultado = desativar_modelo("modelo-inexistente")

        assert resultado is None


def test_buscar_modelo_ativo_existente(client):
    """Deve retornar o modelo atualmente ativo."""
    with patch("application.services.service_llm.LLM") as mock_llm:

        modelo_mock = MagicMock()
        modelo_mock.to_dict.return_value = {"model_id": "modelo-1", "status": "ativada"}
        mock_llm.query.filter_by.return_value.first.return_value = modelo_mock

        from application.services.service_llm import buscar_modelo_ativo
        resultado = buscar_modelo_ativo()

        assert resultado["status"] == "ativada"


def test_buscar_modelo_ativo_nenhum_ativo(client):
    """Deve retornar None quando nenhum modelo estiver ativo."""
    with patch("application.services.service_llm.LLM") as mock_llm:

        mock_llm.query.filter_by.return_value.first.return_value = None

        from application.services.service_llm import buscar_modelo_ativo
        resultado = buscar_modelo_ativo()

        assert resultado is None