"""
Wrapper de integração com o servidor Ollama.

Concentra aqui toda a conversa HTTP com o Ollama para que as camadas de cima
(service_llm) não precisem conhecer detalhes do protocolo. Isso mantém o service
focado em regra de negócio e torna os testes simples: basta mockar este módulo.

Endpoints do Ollama usados:
- POST /api/pull  -> baixa um modelo e transmite o progresso em stream (JSON por linha).

Variável de ambiente:
- OLLAMA_URL: URL base do servidor Ollama (ex.: http://ollama-service:11434).
"""
import json
import os
from typing import Iterator

import httpx
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")

# O download de um modelo pode levar minutos; não faz sentido um timeout curto
# derrubar o stream no meio. O timeout de conexão continua protegendo contra um
# servidor Ollama indisponível.
_PULL_TIMEOUT = httpx.Timeout(connect=10.0, read=None, write=10.0, pool=10.0)


class OllamaModelNotFoundError(Exception):
    """
    Levantada quando o Ollama informa que o modelo solicitado não existe
    (ex.: nome digitado errado ou ausente no registro remoto).
    """
    pass


class OllamaIndisponivelError(Exception):
    """
    Levantada quando não é possível falar com o servidor Ollama
    (offline, URL errada, rede fora do ar).
    """
    pass


def _eh_erro_de_modelo_inexistente(mensagem: str) -> bool:
    """
    Heurística para distinguir "modelo não existe" de outras falhas do Ollama.

    O Ollama responde com mensagens como "pull model manifest: file does not
    exist" ou "model 'x' not found" quando o nome não existe no registro. Não há
    código de erro estruturado, então inspecionamos o texto.
    """
    texto = (mensagem or "").lower()
    indicadores = ("not found", "does not exist", "manifest", "no such")
    return any(indicador in texto for indicador in indicadores)


def _evento_de_linha(linha: str) -> dict:
    """
    Converte uma linha do stream do Ollama em um evento de progresso.

    O Ollama sinaliza falha dentro do próprio stream (não via status HTTP): um
    erro de manifesto/"not found" significa modelo inexistente; qualquer outro
    erro é tratado como indisponibilidade.

    Levanta OllamaModelNotFoundError ou OllamaIndisponivelError conforme o caso.
    """
    dado = json.loads(linha)

    if "error" in dado:
        mensagem = dado["error"]
        if _eh_erro_de_modelo_inexistente(mensagem):
            raise OllamaModelNotFoundError(mensagem)
        raise OllamaIndisponivelError(mensagem)

    return dado


def _erro_de_transporte(exc: httpx.TransportError | httpx.HTTPStatusError) -> Exception:
    """
    Traduz uma falha de transporte do httpx na exceção de domínio adequada.

    Um 404 HTTP também indica modelo inexistente; qualquer outra falha de rede é
    indisponibilidade do servidor.
    """
    resposta = getattr(exc, "response", None)
    if resposta is not None and resposta.status_code == 404:
        return OllamaModelNotFoundError(str(exc))

    return OllamaIndisponivelError(str(exc))


def pull_model(nome: str) -> Iterator[dict]:
    """
    Executa o `pull` de um modelo no Ollama, em stream, e produz os eventos de
    progresso um a um.

    Espera receber:
    - `nome`: str - o nome do modelo a ser baixado (ex.: "llama3").

    Produz (yield) dicionários no formato do Ollama, por exemplo:
        {"status": "pulling manifest"}
        {"status": "downloading ...", "total": 12345, "completed": 678}
        {"status": "success"}

    Levanta:
    - OllamaModelNotFoundError: se o modelo não existir no Ollama.
    - OllamaIndisponivelError: se o servidor Ollama estiver inacessível.
    """
    url = f"{OLLAMA_URL}/api/pull"
    payload = {"name": nome, "stream": True}

    try:
        with httpx.Client(timeout=_PULL_TIMEOUT) as client, \
                client.stream("POST", url, json=payload) as resposta:
            resposta.raise_for_status()
            for linha in resposta.iter_lines():
                if linha:
                    yield _evento_de_linha(linha)
    except (httpx.HTTPStatusError, httpx.RequestError) as exc:
        raise _erro_de_transporte(exc) from exc


def model_exists(nome: str) -> bool:
    """
    Verifica se um modelo existe no Ollama sem baixá-lo por completo.

    A estratégia é sondar o `pull`: abrimos o stream e lemos apenas o primeiro
    evento. Se o Ollama aceitar o pedido (ex.: "pulling manifest"), o modelo
    existe e fechamos a conexão sem concluir o download. Se ele reportar
    "not found", o modelo não existe.

    Espera receber:
    - `nome`: str - o nome do modelo a verificar.

    Retorna:
    - True se o modelo existir no Ollama.
    - False se o modelo não existir.

    Levanta:
    - OllamaIndisponivelError: se o servidor Ollama estiver inacessível.
    """
    eventos = pull_model(nome)
    try:
        # Basta o primeiro evento bem-sucedido para confirmar a existência.
        next(eventos)
        return True
    except OllamaModelNotFoundError:
        return False
    except StopIteration:
        # Stream encerrou sem erro e sem eventos: tratamos como existente,
        # deixando o pull real lidar com qualquer anomalia.
        return True
    finally:
        # Fecha o gerador (e a conexão HTTP subjacente) imediatamente, evitando
        # baixar o modelo inteiro só para checar a existência.
        eventos.close()
