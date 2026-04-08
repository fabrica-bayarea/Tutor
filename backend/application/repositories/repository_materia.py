from application.config.database import db
from application.models.model_arquivo_turma_materia import ArquivoTurmaMateria

def obter_arquivos_por_materia(materia_id: str) -> list[str]:
    """
    Consulta o banco relacional e retorna os IDs dos arquivos
    vinculados à matéria informada.
    """
    registros = db.session.query(ArquivoTurmaMateria).filter_by(
        materia_id=materia_id
    ).all()

    return [str(registro.arquivo_id) for registro in registros]