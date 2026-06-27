"""
Testes do service_llm: CRUD, ativação exclusiva, fluxo de pull e progresso.

Usa um banco SQLite real (apenas a tabela `llm`) para exercitar as transições de
estado de verdade — quem é mockado é só a integração externa com o Ollama
(`repository_ollama`), mantendo os testes rápidos e determinísticos.
"""
import os
import sys
import uuid
from unittest.mock import MagicMock, patch

import pytest

# Garante uma URI de banco e segredo antes de importar `app`, para o import não
# falhar quando o ambiente não define essas variáveis (ex.: CI sem Postgres).
os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/test_service_llm.db")
os.environ.setdefault("SECRET_KEY", "test-secret")

# Stubs das dependências externas pesadas, no mesmo padrão dos demais testes.
sys.modules.setdefault("application.config.vector_database", MagicMock())
sys.modules.setdefault("chromadb", MagicMock())
sys.modules.setdefault("ollama", MagicMock())
sys.modules.setdefault("application.socket.socket_instance", MagicMock())
sys.modules.setdefault("application.socket.event_handler", MagicMock())

from app import app
from application.config.database import db
from application.models.model_llm import LLM
from application.services import service_llm, llm_progress_store
from application.services.service_llm import AddModelErro
from application.repositories.repository_ollama import (
    OllamaModelNotFoundError,
    OllamaIndisponivelError,
)


@pytest.fixture
def ctx():
    """
    Sobe um app_context com o schema recém-criado e limpa ao final.

    Criamos o schema completo (não só `llm`) porque deletar um LLM faz o
    SQLAlchemy carregar o relacionamento reverso `materias` definido em
    model_materia — a tabela precisa existir para o delete não quebrar.
    """
    with app.app_context():
        db.create_all()
        try:
            yield
        finally:
            db.session.remove()
            db.drop_all()


def _criar_llm(nome: str, status: str = "desativada") -> str:
    model_id = str(uuid.uuid4())
    db.session.add(LLM(id=model_id, nome=nome, status=status))
    db.session.commit()
    return model_id


def _fake_pull_eventos():
    """Simula o stream do Ollama: manifesto, dois chunks e o sucesso final."""
    yield {"status": "pulling manifest"}
    yield {"status": "downloading", "total": 100, "completed": 50}
    yield {"status": "downloading", "total": 100, "completed": 100}
    yield {"status": "success"}


# --------------------------------------------------------------------------- #
# addModel
# --------------------------------------------------------------------------- #
def test_add_model_nome_obrigatorio_retorna_erro(ctx):
    modelo, erro = service_llm.addModel({})
    assert modelo is None
    assert erro is AddModelErro.NOME_OBRIGATORIO


def test_add_model_nome_duplicado_retorna_erro(ctx):
    _criar_llm("llama3")
    modelo, erro = service_llm.addModel({"nome": "llama3"})
    assert modelo is None
    assert erro is AddModelErro.NOME_DUPLICADO


def test_add_model_inexistente_remove_registro_e_retorna_404(ctx):
    """Se o Ollama não conhece o modelo, o registro criado deve ser desfeito."""
    with patch.object(service_llm.repository_ollama, "model_exists", return_value=False):
        modelo, erro = service_llm.addModel({"nome": "nao-existe"})

    assert modelo is None
    assert erro is AddModelErro.MODELO_NAO_ENCONTRADO
    # O registro criado durante a tentativa não pode permanecer no banco.
    assert LLM.query.filter_by(nome="nao-existe").first() is None


def test_add_model_existente_cria_registro_e_dispara_pull(ctx):
    with patch.object(service_llm.repository_ollama, "model_exists", return_value=True), \
         patch.object(service_llm, "_iniciar_pull_em_background") as mock_pull:
        modelo, erro = service_llm.addModel({"nome": "llama3"})

    assert erro is None
    assert modelo["nome"] == "llama3"
    assert LLM.query.filter_by(nome="llama3").first() is not None
    # O download deve ser disparado em segundo plano para o id recém-criado.
    mock_pull.assert_called_once()
    assert mock_pull.call_args.args[0] == "llama3"


def test_add_model_ollama_indisponivel_remove_registro(ctx):
    with patch.object(
        service_llm.repository_ollama, "model_exists",
        side_effect=OllamaIndisponivelError("offline"),
    ):
        modelo, erro = service_llm.addModel({"nome": "llama3"})

    assert modelo is None
    assert erro is AddModelErro.OLLAMA_INDISPONIVEL
    assert LLM.query.filter_by(nome="llama3").first() is None


# --------------------------------------------------------------------------- #
# pullModel / progresso
# --------------------------------------------------------------------------- #
def test_pull_model_atualiza_progresso_ate_100(ctx):
    model_id = _criar_llm("llama3")

    with patch.object(
        service_llm.repository_ollama, "pull_model",
        return_value=_fake_pull_eventos(),
    ):
        service_llm.pullModel("llama3", model_id)

    progresso = llm_progress_store.get_progress(model_id)
    assert progresso["percent"] == 100
    assert progresso["status"] == "concluido"


def test_pull_model_modelo_inexistente_marca_status(ctx):
    model_id = _criar_llm("nao-existe")

    with patch.object(
        service_llm.repository_ollama, "pull_model",
        side_effect=OllamaModelNotFoundError("not found"),
    ):
        service_llm.pullModel("nao-existe", model_id)

    progresso = llm_progress_store.get_progress(model_id)
    assert progresso["status"] == "modelo_nao_encontrado"


def test_get_pull_progress_sem_pull_mas_modelo_existe_retorna_100(ctx):
    model_id = _criar_llm("llama3")
    llm_progress_store.clear_progress(model_id)

    progresso = service_llm.getPullProgress(model_id)
    assert progresso == {"percent": 100, "status": "concluido"}


def test_get_pull_progress_id_inexistente_retorna_none(ctx):
    assert service_llm.getPullProgress(str(uuid.uuid4())) is None


def test_pull_all_models_sincroniza_todos(ctx):
    id_a = _criar_llm("llama3")
    id_b = _criar_llm("mistral")

    with patch.object(
        service_llm.repository_ollama, "pull_model",
        side_effect=lambda nome: _fake_pull_eventos(),
    ):
        resumo = service_llm.pullAllModels()

    assert resumo["total"] == 2
    assert set(resumo["sucessos"]) == {"llama3", "mistral"}
    assert resumo["falhas"] == []
    assert llm_progress_store.get_progress(id_a)["percent"] == 100
    assert llm_progress_store.get_progress(id_b)["percent"] == 100


def test_pull_all_models_reporta_falhas(ctx):
    """Modelos que falham no pull devem aparecer em 'falhas', não em 'sucessos'."""
    _criar_llm("llama3")
    _criar_llm("nao-existe")

    def _pull_por_modelo(nome):
        if nome == "nao-existe":
            raise OllamaModelNotFoundError("not found")
        return _fake_pull_eventos()

    with patch.object(
        service_llm.repository_ollama, "pull_model", side_effect=_pull_por_modelo
    ):
        resumo = service_llm.pullAllModels()

    assert resumo["sucessos"] == ["llama3"]
    assert resumo["falhas"] == [
        {"nome": "nao-existe", "status": service_llm.STATUS_MODELO_NAO_ENCONTRADO}
    ]


# --------------------------------------------------------------------------- #
# Ativação exclusiva
# --------------------------------------------------------------------------- #
def test_activate_model_garante_apenas_um_ativo(ctx):
    id_ativo = _criar_llm("llama3", status="ativada")
    id_novo = _criar_llm("mistral", status="desativada")

    with patch.object(service_llm.repository_ollama, "model_installed", return_value=True):
        resultado = service_llm.activateModel(id_novo)

    assert resultado["status"] == "ativada"
    # O antigo ativo deve ter sido desativado.
    assert LLM.query.filter_by(id=id_ativo).first().status == "desativada"
    # Exatamente um modelo ativo no total.
    assert LLM.query.filter_by(status="ativada").count() == 1


def test_activate_model_inexistente_retorna_none(ctx):
    assert service_llm.activateModel(str(uuid.uuid4())) is None


def test_activate_model_nao_instalado_levanta_erro(ctx):
    """Ativar um modelo não instalado no Ollama falha e não altera o banco."""
    id_modelo = _criar_llm("fantasma", status="desativada")

    with patch.object(
        service_llm.repository_ollama, "model_installed", return_value=False
    ):
        with pytest.raises(service_llm.ModeloNaoInstaladoError):
            service_llm.activateModel(id_modelo)

    assert LLM.query.filter_by(id=id_modelo).first().status == "desativada"


# --------------------------------------------------------------------------- #
# CRUD básico
# --------------------------------------------------------------------------- #
def test_update_model_altera_nome(ctx):
    model_id = _criar_llm("llama3")
    atualizado = service_llm.updateModel(model_id, {"nome": "llama3.1"})
    assert atualizado["nome"] == "llama3.1"


def test_delete_model_remove_e_limpa_progresso(ctx):
    model_id = _criar_llm("llama3")
    llm_progress_store.set_progress(model_id, 42, "baixando")

    removido = service_llm.deleteModel(model_id)

    assert removido["nome"] == "llama3"
    assert LLM.query.filter_by(id=model_id).first() is None
    assert llm_progress_store.get_progress(model_id) is None


def test_get_all_models_retorna_lista(ctx):
    _criar_llm("llama3")
    _criar_llm("mistral")
    modelos = service_llm.getAllModels()
    assert {m["nome"] for m in modelos} == {"llama3", "mistral"}
