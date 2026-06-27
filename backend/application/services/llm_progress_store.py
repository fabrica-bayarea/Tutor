"""
Armazenamento em memória do progresso do `pull` de modelos LLM.

O download de um modelo no Ollama roda numa thread de fundo (ver service_llm), e
o frontend acompanha o andamento por polling na rota `/llm/pull-status/<id>`.
Como o progresso é um estado efêmero (não precisa sobreviver a reinícios nem ser
consultado por outros serviços), guardá-lo no banco seria exagero: usamos um
dicionário em memória protegido por lock.

Limitação consciente: o estado vive no processo. Numa implantação com múltiplos
workers, cada um teria seu próprio mapa. Para o cenário single-process atual do
backend isso é suficiente; se a infraestrutura mudar, este módulo é o único ponto
a trocar por Redis/cache compartilhado.
"""
import threading

# id_do_modelo -> {"percent": int, "status": str}
_progresso: dict[str, dict] = {}
_lock = threading.Lock()


def set_progress(model_id: str, percent: int, status: str) -> None:
    """
    Registra (ou atualiza) o progresso do pull de um modelo.

    Espera receber:
    - `model_id`: str - id do modelo no banco.
    - `percent`: int - percentual concluído (0–100).
    - `status`: str - rótulo legível do estágio atual (ex.: "baixando", "erro").
    """
    # Garante que o percentual fique sempre dentro de 0–100, independentemente
    # do que o Ollama reportar, para o frontend nunca receber valor inválido.
    percent = max(0, min(100, int(percent)))

    with _lock:
        _progresso[str(model_id)] = {"percent": percent, "status": status}


def get_progress(model_id: str) -> dict | None:
    """
    Retorna o progresso atual de um modelo.

    Retorna um dicionário {"percent": int, "status": str} se houver um pull
    registrado para o id, e None caso contrário.
    """
    with _lock:
        progresso = _progresso.get(str(model_id))
        # Devolve uma cópia para o chamador não alterar o estado interno por engano.
        return dict(progresso) if progresso else None


def clear_progress(model_id: str) -> None:
    """
    Remove o progresso de um modelo (ex.: quando o registro é deletado).
    """
    with _lock:
        _progresso.pop(str(model_id), None)
