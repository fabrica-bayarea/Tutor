from application.config.database import db
from application.models.model_materia import Materia


class ModelRouter:

    def __init__(self, registry):
        self.registry = registry


    def resolve(self, materia_id: str) -> dict:

        materia = Materia.query.filter_by(id=materia_id).first()

        if not materia:
            raise ValueError("Matéria não encontrada")

        llm_id = materia.llm_id

        return self.registry.get(llm_id)