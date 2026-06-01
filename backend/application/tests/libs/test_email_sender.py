"""
Testes unitários do envio de e-mail (convite e recuperação de senha).

O SMTP é totalmente mockado — nenhum e-mail/conexão real é feito. Cobrem:
- retry com sucesso, retry esgotado e o guard que evita `raise None`;
- montagem das mensagens de convite e de recuperação;
- disparo assíncrono (thread) com tratamento de erro.
"""
import sys
from unittest.mock import MagicMock, patch

sys.modules.setdefault("chromadb", MagicMock())
sys.modules.setdefault("ollama", MagicMock())
sys.modules.setdefault("application.config.vector_database", MagicMock())

import pytest
import application.libs.email_sender as es


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    """Evita esperas reais entre tentativas."""
    monkeypatch.setattr(es.time, "sleep", lambda *_: None)


def _smtp_context(server):
    """Cria um mock de smtplib.SMTP usado como context manager (`with ... as`)."""
    cm = MagicMock()
    cm.__enter__.return_value = server
    cm.__exit__.return_value = False
    return cm


# ---------------------------------------------------------------------------
# _enviar_mensagem — retry / guard
# ---------------------------------------------------------------------------

def test_envia_na_primeira_tentativa(monkeypatch):
    server = MagicMock()
    smtp = MagicMock(return_value=_smtp_context(server))
    monkeypatch.setattr(es.smtplib, "SMTP", smtp)

    es._enviar_mensagem(MagicMock(), "dest@iesb.edu.br")

    smtp.assert_called_once()
    server.login.assert_called_once()
    server.sendmail.assert_called_once()


def test_reenvia_apos_falha_transitoria(monkeypatch):
    server_ok = MagicMock()
    # 1ª tentativa falha ao abrir conexão; 2ª funciona.
    smtp = MagicMock(side_effect=[Exception("timeout"), _smtp_context(server_ok)])
    monkeypatch.setattr(es.smtplib, "SMTP", smtp)
    monkeypatch.setattr(es, "SMTP_TENTATIVAS", 3)

    es._enviar_mensagem(MagicMock(), "dest@iesb.edu.br")

    assert smtp.call_count == 2
    server_ok.sendmail.assert_called_once()


def test_levanta_ultimo_erro_quando_todas_falham(monkeypatch):
    smtp = MagicMock(side_effect=RuntimeError("smtp fora do ar"))
    monkeypatch.setattr(es.smtplib, "SMTP", smtp)
    monkeypatch.setattr(es, "SMTP_TENTATIVAS", 2)

    with pytest.raises(RuntimeError, match="smtp fora do ar"):
        es._enviar_mensagem(MagicMock(), "dest@iesb.edu.br")
    assert smtp.call_count == 2


def test_sem_tentativas_levanta_runtimeerror_explicito(monkeypatch):
    # Guard contra `raise None`: se o laço nunca executa, erra de forma explícita.
    monkeypatch.setattr(es, "SMTP_TENTATIVAS", 0)
    smtp = MagicMock()
    monkeypatch.setattr(es.smtplib, "SMTP", smtp)

    with pytest.raises(RuntimeError, match="nenhuma tentativa"):
        es._enviar_mensagem(MagicMock(), "dest@iesb.edu.br")
    smtp.assert_not_called()


# ---------------------------------------------------------------------------
# Montagem das mensagens (convite e recuperação)
# ---------------------------------------------------------------------------

def test_enviar_email_convite_monta_e_envia(monkeypatch):
    enviar = MagicMock()
    monkeypatch.setattr(es, "_enviar_mensagem", enviar)

    es.enviar_email_convite("aluno@iesb.edu.br", "Maria Silva", "token-123")

    enviar.assert_called_once()
    msg, destinatario = enviar.call_args.args
    assert destinatario == "aluno@iesb.edu.br"
    assert msg["To"] == "aluno@iesb.edu.br"
    html = msg.get_payload()[0].get_payload(decode=True).decode()
    assert "token-123" in html


def test_enviar_email_recuperacao_monta_e_envia(monkeypatch):
    enviar = MagicMock()
    monkeypatch.setattr(es, "_enviar_mensagem", enviar)

    es.enviar_email_recuperacao_senha("aluno@iesb.edu.br", "João", "tok-reset")

    enviar.assert_called_once()
    msg, destinatario = enviar.call_args.args
    assert destinatario == "aluno@iesb.edu.br"
    html = msg.get_payload()[0].get_payload(decode=True).decode()
    assert "reset=1" in html
    assert "tok-reset" in html


# ---------------------------------------------------------------------------
# Disparo assíncrono
# ---------------------------------------------------------------------------

def _thread_sincrona(monkeypatch):
    """Faz Thread.start() rodar o target de forma síncrona."""
    def fake_thread(target=None, daemon=None, **_):
        t = MagicMock()
        t.start.side_effect = lambda: target()
        return t
    monkeypatch.setattr(es.threading, "Thread", fake_thread)


def test_envio_async_chama_envio_convite(monkeypatch):
    _thread_sincrona(monkeypatch)
    convite = MagicMock()
    monkeypatch.setattr(es, "enviar_email_convite", convite)

    es.enviar_email_convite_async("a@iesb.edu.br", "Ana", "tok")

    convite.assert_called_once_with("a@iesb.edu.br", "Ana", "tok")


def test_envio_async_loga_e_nao_propaga_erro(monkeypatch):
    _thread_sincrona(monkeypatch)
    monkeypatch.setattr(es, "enviar_email_convite", MagicMock(side_effect=Exception("falhou")))

    # Não deve propagar a exceção (apenas registra em log).
    es.enviar_email_convite_async("a@iesb.edu.br", "Ana", "tok")
