"""
Regras de negócio para gestão de modelos de IA (LLM).

Responsabilidades:
- CRUD dos registros de LLM no banco relacional.
- Garantir que apenas um modelo fique ativo por vez.
- Orquestrar o `pull` (download) de modelos no Ollama, atualizando o progresso
  consultado por polling em `/llm/pull-status/<id>`.

A conversa HTTP com o Ollama fica isolada em `repositories/repository_ollama.py`
e o progresso efêmero do download em `services/llm_progress_store.py`.
"""
import threading
import uuid
from enum import Enum

from application.config.database import db
from application.models import LLM
from application.repositories import repository_ollama
from application.repositories.repository_ollama import (
    OllamaModelNotFoundError,
    OllamaIndisponivelError,
)
from application.services import llm_progress_store


class AddModelErro(Enum):
    """
    Resultados de falha possíveis ao adicionar um modelo.

    Usar um Enum (em vez de strings soltas) torna o contrato entre service e rota
    explícito e à prova de erro de digitação: a rota despacha cada membro para a
    resposta HTTP correspondente via um dicionário (ver route_llm).
    """
    NOME_OBRIGATORIO = "nome_obrigatorio"
    NOME_DUPLICADO = "nome_duplicado"
    MODELO_NAO_ENCONTRADO = "modelo_nao_encontrado"
    OLLAMA_INDISPONIVEL = "ollama_indisponivel"


# Status terminais de um `pull`, gravados no progress store e usados como contrato
# entre o service e quem observa o resultado (rota de polling e boot da aplicação).
# Centralizados aqui para evitar strings mágicas espalhadas.
STATUS_CONCLUIDO = "concluido"
STATUS_ERRO = "erro"
STATUS_MODELO_NAO_ENCONTRADO = "modelo_nao_encontrado"


class ModeloNaoInstaladoError(Exception):
    """
    Levantada ao tentar ativar um modelo que não está instalado no Ollama.

    Garante a regra da US-38: só é possível ativar um modelo cujo download foi
    concluído — impede ativar registros órfãos ou cujo pull falhou.
    """
    pass


# --------------------------------------------------------------------------- #
# Leitura
# --------------------------------------------------------------------------- #
def getAllModels() -> list[dict]:
    """
    Lista todos os modelos de IA cadastrados.

    Retorna uma lista de dicionários (vazia se não houver modelos).
    """
    modelos = LLM.query.order_by(LLM.nome.asc()).all()
    return [modelo.to_dict() for modelo in modelos]


def getModelById(model_id: str) -> dict | None:
    """
    Busca um modelo de IA pelo seu ID.

    Espera receber:
    - `model_id`: str - o ID do modelo.

    Retorna o modelo se ele existir, e None caso contrário.
    """
    modelo = LLM.query.filter_by(id=str(model_id)).first()
    return modelo.to_dict() if modelo else None


# --------------------------------------------------------------------------- #
# Escrita / CRUD
# --------------------------------------------------------------------------- #
def updateModel(model_id: str, data: dict) -> dict | None:
    """
    Atualiza os dados editáveis de um modelo (apenas `nome`).

    Espera receber:
    - `model_id`: str - o ID do modelo.
    - `data`: dict - campos a atualizar; hoje só `nome` é editável. O `status`
      é controlado pelo fluxo de ativação (`activateModel`), não por aqui.

    Retorna o modelo atualizado se ele existir, e None caso contrário.
    """
    modelo = LLM.query.filter_by(id=str(model_id)).first()
    if not modelo:
        return None

    novo_nome = (data or {}).get("nome")
    if novo_nome:
        modelo.nome = novo_nome

    db.session.commit()
    return modelo.to_dict()


def deleteModel(model_id: str) -> dict | None:
    """
    Remove um modelo de IA do banco.

    Espera receber:
    - `model_id`: str - o ID do modelo.

    Também limpa qualquer progresso de pull associado, evitando que a rota de
    polling continue reportando estado de um modelo que não existe mais.

    Retorna o modelo removido se ele existia, e None caso contrário.
    """
    modelo = LLM.query.filter_by(id=str(model_id)).first()
    if not modelo:
        return None

    dados = modelo.to_dict()
    db.session.delete(modelo)
    db.session.commit()

    llm_progress_store.clear_progress(model_id)
    return dados


def activateModel(model_id: str) -> dict | None:
    """
    Ativa um modelo de IA, garantindo que apenas um fique ativo por vez.

    Espera receber:
    - `model_id`: str - o ID do modelo a ser ativado.

    Só ativa um modelo de fato instalado no Ollama (US-38): isso impede ativar
    registros cujo download falhou ou que nunca existiram. Desativa qualquer
    modelo atualmente ativo antes de ativar o novo.

    Retorna o modelo ativado, ou None se o id não existir.

    Levanta:
    - ModeloNaoInstaladoError: se o modelo não estiver instalado no Ollama.
    - OllamaIndisponivelError: se o servidor Ollama estiver inacessível.
    """
    modelo = LLM.query.filter_by(id=str(model_id)).first()
    if not modelo:
        return None

    # Confirma que o modelo está realmente instalado antes de ativar — sem isso,
    # registros órfãos (pull que falhou) poderiam virar o modelo ativo.
    if not repository_ollama.model_installed(modelo.nome):
        raise ModeloNaoInstaladoError(modelo.nome)

    # Desativa todos os ativos antes de ativar o alvo: é o que garante a regra
    # "apenas um modelo ativo por vez".
    LLM.query.filter_by(status="ativada").update({"status": "desativada"})
    modelo.status = "ativada"
    db.session.commit()

    return modelo.to_dict()


def _validar_dados_novo_modelo(data: dict) -> AddModelErro | None:
    """
    Valida o payload de criação de um modelo, sem efeitos colaterais.

    Retorna o `AddModelErro` correspondente à primeira regra violada, ou None se
    os dados forem válidos. Extraído de `addModel` para manter aquela função
    enxuta (uma responsabilidade: orquestrar a criação + pull).
    """
    nome = (data or {}).get("nome")
    if not nome:
        return AddModelErro.NOME_OBRIGATORIO

    if LLM.query.filter_by(nome=nome).first():
        return AddModelErro.NOME_DUPLICADO

    return None


def addModel(data: dict) -> tuple[dict | None, AddModelErro | None]:
    """
    Adiciona um novo modelo: cria o registro e dispara o `pull` no Ollama.

    Fluxo (conforme US-38.3):
    1. Valida o nome e impede nomes duplicados.
    2. Cria o registro no banco (status inicial 'desativada').
    3. Verifica se o modelo existe no Ollama. Se NÃO existir, desfaz o registro
       e sinaliza erro (a rota traduz para HTTP 404).
    4. Se existir, dispara o download numa thread de fundo e retorna o registro
       imediatamente; o progresso é acompanhado por polling.

    Espera receber:
    - `data`: dict - deve conter `nome` (o nome do modelo no Ollama).

    Retorna uma tupla `(modelo, erro)`:
    - `(modelo_dict, None)` em caso de sucesso.
    - `(None, AddModelErro.*)` na falha correspondente (a rota despacha o membro
      do Enum para o status HTTP adequado).
    """
    erro = _validar_dados_novo_modelo(data)
    if erro is not None:
        return None, erro

    nome = data["nome"]
    modelo = LLM(id=str(uuid.uuid4()), nome=nome, status="desativada")
    db.session.add(modelo)
    db.session.commit()

    model_id = modelo.id

    # Semeia o progresso em 0% já na criação, para a rota de polling ter algo a
    # reportar mesmo antes de a thread de download começar de fato.
    llm_progress_store.set_progress(model_id, 0, "iniciando")

    try:
        existe = repository_ollama.model_exists(nome)
    except OllamaIndisponivelError:
        # Não dá para validar nem baixar: desfaz o registro recém-criado para não
        # deixar lixo no banco.
        deleteModel(model_id)
        return None, AddModelErro.OLLAMA_INDISPONIVEL

    if not existe:
        # Regra da issue: se o modelo não existe no Ollama, o registro criado é
        # removido e a rota responde 404.
        deleteModel(model_id)
        return None, AddModelErro.MODELO_NAO_ENCONTRADO

    _iniciar_pull_em_background(nome, model_id)
    return modelo.to_dict(), None


# --------------------------------------------------------------------------- #
# Pull / progresso
# --------------------------------------------------------------------------- #
def _iniciar_pull_em_background(nome: str, model_id: str) -> None:
    """
    Dispara `pullModel` numa thread daemon, para o download não bloquear a
    resposta HTTP. A thread só escreve no progress store (memória), então não
    precisa de app context nem acessa o banco.
    """
    thread = threading.Thread(
        target=pullModel,
        args=(nome, model_id),
        daemon=True,
    )
    thread.start()


def _percentual_do_evento(evento: dict, percent_atual: int) -> int:
    """
    Calcula o percentual concluído a partir de um evento de progresso do Ollama.

    Nem todo evento traz `total`/`completed` (ex.: "pulling manifest"); nesses
    casos preserva-se o último percentual conhecido.
    """
    total = evento.get("total")
    if not total:
        return percent_atual

    return int((evento.get("completed") or 0) / total * 100)


def pullModel(nome: str, model_id: str) -> str:
    """
    Executa o `pull` de um modelo no Ollama e atualiza o progresso (0–100%).

    Espera receber:
    - `nome`: str - o nome do modelo no Ollama.
    - `model_id`: str - o ID do registro, usado como chave no progress store.

    Nunca levanta exceção (é seguro chamar numa thread de fundo). Retorna o status
    terminal: `STATUS_CONCLUIDO` em sucesso, ou `STATUS_ERRO` /
    `STATUS_MODELO_NAO_ENCONTRADO` em falha. O progresso também fica observável via
    `getPullProgress(model_id)`.
    """
    percent_atual = 0
    try:
        for evento in repository_ollama.pull_model(nome):
            percent_atual = _percentual_do_evento(evento, percent_atual)
            llm_progress_store.set_progress(
                model_id, percent_atual, evento.get("status", "baixando")
            )

        # O stream terminou sem erro: o download está completo.
        llm_progress_store.set_progress(model_id, 100, STATUS_CONCLUIDO)
        return STATUS_CONCLUIDO
    except OllamaModelNotFoundError:
        llm_progress_store.set_progress(model_id, percent_atual, STATUS_MODELO_NAO_ENCONTRADO)
        return STATUS_MODELO_NAO_ENCONTRADO
    except OllamaIndisponivelError:
        llm_progress_store.set_progress(model_id, percent_atual, STATUS_ERRO)
        return STATUS_ERRO


def pullAllModels() -> dict:
    """
    Sincroniza todos os modelos cadastrados com o Ollama, executando o `pull`
    de cada um sequencialmente (uso no boot da aplicação e administrativo).

    Diferente de `addModel`, roda de forma síncrona — a intenção é garantir que
    todas as imagens estejam presentes antes de prosseguir.

    Retorna um agregado para o chamador decidir o que fazer (ex.: bloquear o boot
    se houver falhas):
        {
            "total": int,
            "sucessos": [nome, ...],
            "falhas": [{"nome": str, "status": str}, ...],
        }
    """
    modelos = getAllModels()
    sucessos: list[str] = []
    falhas: list[dict] = []

    for modelo in modelos:
        status = pullModel(modelo["nome"], modelo["id"])
        if status == STATUS_CONCLUIDO:
            sucessos.append(modelo["nome"])
        else:
            falhas.append({"nome": modelo["nome"], "status": status})

    return {"total": len(modelos), "sucessos": sucessos, "falhas": falhas}


def getPullProgress(model_id: str) -> dict | None:
    """
    Retorna o progresso atual do `pull` de um modelo, para a rota de polling.

    Espera receber:
    - `model_id`: str - o ID do modelo.

    Retorna:
    - {"percent": int, "status": str} se houver um pull registrado.
    - {"percent": 100, "status": "concluido"} se o modelo existe no banco mas não
      há pull em andamento (assume-se que já foi baixado anteriormente).
    - None se o id não corresponde a nenhum modelo (a rota traduz para 404).
    """
    progresso = llm_progress_store.get_progress(model_id)
    if progresso is not None:
        return progresso

    # Sem progresso em memória: distingue "modelo já baixado" de "id inexistente".
    if getModelById(model_id) is not None:
        return {"percent": 100, "status": STATUS_CONCLUIDO}

    return None


# --------------------------------------------------------------------------- #
# Leitura do modelo ativo (consumido pelo fluxo de chat)
# --------------------------------------------------------------------------- #
def getActiveModel() -> str | None:
    """
    Retorna apenas o nome do modelo ativo.

    Utilizado pelo fluxo de chat e por outros serviços que precisam saber qual
    modelo está em uso sem precisar do objeto completo.

    Retorna o nome do modelo ativo, ou None se não houver nenhum.
    """
    modelo = LLM.query.filter_by(status="ativada").first()
    return modelo.nome if modelo else None
