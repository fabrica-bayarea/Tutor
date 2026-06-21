"""
Testes do fluxo de pull dos modelos na inicialização (US-38.4).

Exercita `sincronizar_modelos_no_boot` diretamente (sem importar `app`), com
`pullAllModels` mockado — assim cobrimos todos os critérios de aceitação sem tocar
no Ollama nem no banco.
"""
import logging
from unittest.mock import MagicMock, patch

import pytest

from application import startup


def _app_falso() -> MagicMock:
    """App fake cujo `app_context()` funciona como context manager (no-op)."""
    return MagicMock()


def test_no_op_quando_flag_desligada(monkeypatch):
    """
    Sem a flag, o boot NÃO deve chamar pullAllModels — é o que protege a suíte de
    testes e o `flask run` local de dispararem downloads.
    """
    monkeypatch.delenv(startup.FLAG_PULL_NO_BOOT, raising=False)

    with patch.object(startup, "pullAllModels") as mock_pull:
        startup.sincronizar_modelos_no_boot(_app_falso())

    mock_pull.assert_not_called()


def test_no_op_durante_migracao_mesmo_com_flag_ligada(monkeypatch):
    """
    Mesmo com a flag ligada, comandos `flask db ...` (ex.: o `flask db upgrade` do
    entrypoint) NÃO devem disparar o pull — a tabela `llm` ainda não existe nesse
    momento (problema ovo-e-galinha).
    """
    monkeypatch.setenv(startup.FLAG_PULL_NO_BOOT, "true")
    monkeypatch.setattr(startup.sys, "argv", ["flask", "db", "upgrade"])

    with patch.object(startup, "pullAllModels") as mock_pull:
        startup.sincronizar_modelos_no_boot(_app_falso())

    mock_pull.assert_not_called()


def test_chama_pull_all_models_quando_flag_ligada(monkeypatch):
    """Com a flag ligada, o boot deve sincronizar via pullAllModels."""
    monkeypatch.setenv(startup.FLAG_PULL_NO_BOOT, "true")

    with patch.object(
        startup, "pullAllModels",
        return_value={"total": 1, "sucessos": ["llama3"], "falhas": []},
    ) as mock_pull:
        startup.sincronizar_modelos_no_boot(_app_falso())

    mock_pull.assert_called_once()


def test_bloqueia_inicializacao_quando_ha_falha(monkeypatch):
    """Qualquer falha de pull deve levantar RuntimeError (bloqueia o boot)."""
    monkeypatch.setenv(startup.FLAG_PULL_NO_BOOT, "1")

    resultado = {
        "total": 2,
        "sucessos": ["llama3"],
        "falhas": [{"nome": "nao-existe", "status": "modelo_nao_encontrado"}],
    }

    with patch.object(startup, "pullAllModels", return_value=resultado):
        with pytest.raises(RuntimeError, match="nao-existe"):
            startup.sincronizar_modelos_no_boot(_app_falso())


def test_nao_bloqueia_quando_todos_concluem(monkeypatch):
    """Sem falhas, a inicialização segue normalmente (sem exceção)."""
    monkeypatch.setenv(startup.FLAG_PULL_NO_BOOT, "on")

    resultado = {"total": 2, "sucessos": ["llama3", "mistral"], "falhas": []}

    with patch.object(startup, "pullAllModels", return_value=resultado):
        # Não deve levantar.
        startup.sincronizar_modelos_no_boot(_app_falso())


def test_loga_status_de_cada_pull(monkeypatch, caplog):
    """Os logs de inicialização devem mostrar o status de cada pull (sucesso/falha)."""
    monkeypatch.setenv(startup.FLAG_PULL_NO_BOOT, "true")

    resultado = {
        "total": 2,
        "sucessos": ["llama3"],
        "falhas": [{"nome": "nao-existe", "status": "erro"}],
    }

    with patch.object(startup, "pullAllModels", return_value=resultado):
        with caplog.at_level(logging.INFO, logger="application.startup"):
            with pytest.raises(RuntimeError):
                startup.sincronizar_modelos_no_boot(_app_falso())

    texto = caplog.text
    assert "llama3" in texto                       # status de sucesso logado
    assert "nao-existe" in texto                   # status de falha logado
    # A falha precisa ser registrada em nível de erro.
    assert any(r.levelno == logging.ERROR for r in caplog.records)
