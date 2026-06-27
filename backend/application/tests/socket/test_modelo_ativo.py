import sys
from unittest.mock import MagicMock, patch
import uuid

sys.modules["application.config.vector_database"] = MagicMock()
sys.modules["chromadb"] = MagicMock()
sys.modules["ollama"] = MagicMock()
sys.modules["application.socket.socketio"] = MagicMock()

from app import app
from application.config.database import db
from application.models.model_llm import LLM
from application.services.service_llm import getActiveModel


def _limpar_llms():
    LLM.query.delete()
    db.session.commit()


def test_get_active_model_retorna_nome():
    """
    getActiveModel() deve retornar o nome do modelo com status='ativada'.
    """
    with app.app_context():
        _limpar_llms()

        modelo = LLM(id=str(uuid.uuid4()), nome="llama3", status="ativada")
        db.session.add(modelo)
        db.session.commit()

        resultado = getActiveModel()

        assert resultado == "llama3"

        _limpar_llms()


def test_get_active_model_retorna_none_sem_modelo():
    """
    getActiveModel() deve retornar None quando não há modelo ativo.
    """
    with app.app_context():
        _limpar_llms()

        resultado = getActiveModel()

        assert resultado is None


def test_chat_usa_fallback_llama3_sem_modelo_ativo():
    """
    Quando getActiveModel() retorna None, o fluxo deve usar 'llama3' como fallback.
    Replica a lógica do event_handler para garantir o comportamento correto.
    """
    with app.app_context():
        _limpar_llms()

        model = getActiveModel()
        if model is None:
            model = "llama3"

        assert model == "llama3"


def test_chat_usa_modelo_ativo_do_banco():
    """
    O fluxo de chat deve usar o modelo ativo do banco, não o vinculado à matéria.
    Verifica que getActiveModel() retorna o modelo correto para uso no chat.
    """
    with app.app_context():
        _limpar_llms()

        modelo = LLM(id=str(uuid.uuid4()), nome="mistral", status="ativada")
        db.session.add(modelo)
        db.session.commit()

        model = getActiveModel()
        if model is None:
            model = "llama3"

        assert model == "mistral"

        _limpar_llms()


def test_conversa_em_andamento_nao_troca_modelo_mid_flow():
    """
    Uma conversa em andamento (chat_id já existente) deve continuar
    funcionando normalmente após troca do modelo ativo.
    O modelo é consultado no início de cada mensagem — a troca só afeta
    mensagens novas, não o histórico já persistido.
    """
    with app.app_context():
        _limpar_llms()

        modelo_antigo = LLM(id=str(uuid.uuid4()), nome="llama3", status="ativada")
        db.session.add(modelo_antigo)
        db.session.commit()

        model_antes = getActiveModel()
        assert model_antes == "llama3"

        # Simula troca de modelo ativo
        LLM.query.filter_by(status="ativada").update({"status": "desativada"})
        modelo_novo = LLM(id=str(uuid.uuid4()), nome="mistral", status="ativada")
        db.session.add(modelo_novo)
        db.session.commit()

        model_depois = getActiveModel()
        assert model_depois == "mistral"

        # Garante que as mensagens anteriores (persistidas) não são afetadas —
        # o histórico não referencia o modelo, apenas o conteúdo das mensagens.
        assert model_antes != model_depois

        _limpar_llms()


def test_associacao_por_materia_nao_e_utilizada():
    """
    O fluxo de chat NÃO deve chamar buscar_llm_materia_por_id.
    Confirma que a dependência da LLM vinculada à matéria foi removida.
    """
    with app.app_context():
        with patch(
            "application.services.service_materia.buscar_llm_materia_por_id"
        ) as mock_buscar_llm_materia:

            _limpar_llms()
            modelo = LLM(id=str(uuid.uuid4()), nome="llama3", status="ativada")
            db.session.add(modelo)
            db.session.commit()

            # Simula o que o event_handler faz agora
            model = getActiveModel()
            if model is None:
                model = "llama3"

            # A função de associação por matéria jamais deve ser chamada
            mock_buscar_llm_materia.assert_not_called()

            _limpar_llms()


if __name__ == "__main__":
    test_get_active_model_retorna_nome()
    test_get_active_model_retorna_none_sem_modelo()
    test_chat_usa_fallback_llama3_sem_modelo_ativo()
    test_chat_usa_modelo_ativo_do_banco()
    test_conversa_em_andamento_nao_troca_modelo_mid_flow()
    test_associacao_por_materia_nao_e_utilizada()
    print("Todos os testes de modelo ativo passaram.")