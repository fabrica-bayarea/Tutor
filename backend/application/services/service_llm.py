from application.config.database import db
from application.models import LLM


def ativar_modelo(model_id: str) -> dict | None:
    """
    Ativa um modelo de IA, garantindo que apenas um fique ativo por vez.

    Espera receber:
    - `model_id`: str - o ID do modelo a ser ativado

    Desativa qualquer modelo atualmente ativo antes de ativar o novo.

    Retorna o modelo ativado se ele existir, e None caso contrário.
    """
    modelo = LLM.query.filter_by(id=model_id).first()
    if not modelo:
        return None

    LLM.query.filter_by(status='ativada').update({'status': 'desativada'})
    modelo.status = 'ativada'
    db.session.commit()

    return modelo.to_dict()


def desativar_modelo(model_id: str) -> dict | None:
    """
    Desativa um modelo de IA.

    Espera receber:
    - `model_id`: str - o ID do modelo a ser desativado

    Retorna o modelo desativado se ele existir, e None caso contrário.
    """
    modelo = LLM.query.filter_by(id=model_id).first()
    if not modelo:
        return None

    modelo.status = 'desativada'
    db.session.commit()

    return modelo.to_dict()


def buscar_modelo_ativo() -> dict | None:
    """
    Busca o modelo de IA atualmente ativo.

    Retorna o modelo ativo se existir, e None caso contrário.
    """
    modelo = LLM.query.filter_by(status='ativada').first()
    return modelo.to_dict() if modelo else None

def getActiveModel() -> str:
    """
    Retorna apenas o nome do modelo ativo.

    Utilizado pelo fluxo de chat e por outros serviços que precisam
    saber qual modelo está em uso sem precisar do objeto completo.

    Retorna o nome do modelo ativo, ou None se não houver nenhum.
    """
    modelo = LLM.query.filter_by(status='ativada').first()
    return modelo.nome if modelo else None