"""
Rotinas de inicialização (boot) da aplicação.

Concentra aqui o que precisa rodar uma única vez, ao subir o servidor, antes de
ele atender requisições. Hoje: sincronizar com o Ollama todos os modelos de IA
cadastrados no banco (US-38.4).

A sincronização é **opt-in** por variável de ambiente para não disparar durante a
suíte de testes nem no `flask run` local — onde `from app import app` executaria
este código sem um Ollama disponível. Em produção, o docker-compose liga a flag.
"""
import logging
import os
import sys

from application.services.service_llm import pullAllModels

logger = logging.getLogger(__name__)

# Variável de ambiente que habilita o pull no boot. Ligada no docker-compose do
# deploy; ausente/desligada em testes e desenvolvimento local.
FLAG_PULL_NO_BOOT = "PULL_MODELS_ON_STARTUP"

_VALORES_VERDADEIROS = {"1", "true", "yes", "on"}


def _pull_no_boot_habilitado() -> bool:
    """Indica se o pull de modelos no boot está habilitado pela variável de ambiente."""
    # Comandos de migração (`flask db ...`) importam o app antes de a tabela `llm`
    # existir; nesse caso o pull não pode rodar — evita o problema ovo-e-galinha.
    if len(sys.argv) > 1 and sys.argv[1] == "db":
        return False
    return os.getenv(FLAG_PULL_NO_BOOT, "").strip().lower() in _VALORES_VERDADEIROS


def _logar_resultado_pull(resultado: dict) -> None:
    """Registra nos logs o status de cada pull (sucesso em info, falha em error)."""
    for nome in resultado["sucessos"]:
        logger.info("Pull concluído: modelo '%s' sincronizado.", nome)

    for falha in resultado["falhas"]:
        logger.error(
            "Pull falhou: modelo '%s' (status: %s).", falha["nome"], falha["status"]
        )


def sincronizar_modelos_no_boot(app) -> None:
    """
    Sincroniza com o Ollama todos os modelos cadastrados, durante a inicialização.

    Regras (US-38.4):
    - Só executa se a flag `PULL_MODELS_ON_STARTUP` estiver ligada (caso contrário,
      é um no-op — protege testes e dev local).
    - Registra nos logs o status de cada pull realizado.
    - Se algum pull falhar, levanta `RuntimeError` para **bloquear a inicialização**
      até o problema ser resolvido (a aplicação não deve atender requisições com
      modelos dessincronizados).

    Espera receber:
    - `app`: a instância Flask, para abrir o app_context necessário ao acesso ao banco.
    """
    if not _pull_no_boot_habilitado():
        logger.debug(
            "Pull de modelos no boot desabilitado (defina %s para habilitar).",
            FLAG_PULL_NO_BOOT,
        )
        return

    logger.info("Sincronizando modelos de IA com o Ollama na inicialização...")

    # pullAllModels consulta o banco (getAllModels), então precisa de app_context.
    with app.app_context():
        resultado = pullAllModels()

    _logar_resultado_pull(resultado)

    if resultado["falhas"]:
        nomes_falha = ", ".join(falha["nome"] for falha in resultado["falhas"])
        raise RuntimeError(
            "Inicialização bloqueada: falha ao sincronizar com o Ollama os modelos: "
            f"{nomes_falha}. Resolva o problema e reinicie a aplicação."
        )

    logger.info(
        "Sincronização concluída: %d modelo(s) prontos.", len(resultado["sucessos"])
    )
