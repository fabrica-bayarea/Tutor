import uuid
from application.models import Materia
from application.models.model_materia import StatusMateriaEnum
from application.config.database import db

def buscar_materia_por_id(materia_id: uuid.UUID = None) -> dict | None:
    """
    Busca uma matéria no banco de dados usando seu ID.

    Espera receber:
    - `materia_id`: uuid.UUID - o ID da matéria
    
    Retorna a matéria se ela existir, e None caso contrário.
    """
    materia = Materia.query.filter_by(id=materia_id).first()
    return materia.to_dict() if materia else None

def buscar_id_materia_por_codigo(codigo_materia: str) -> uuid.UUID | None:
    """
    Busca uma matéria no banco de dados usando o código fornecido.

    Espera receber:
    - `codigo_materia`: str - o código da matéria
    
    Retorna o UUID da matéria se ela existir, e None caso contrário.
    """
    materia = Materia.query.filter_by(codigo=codigo_materia).first()
    return materia.id if materia else None

def buscar_codigo_materia_por_id(id_materia: uuid.UUID) -> str | None:
    """
    Busca uma matéria no banco de dados usando o ID fornecido.

    Espera receber:
    - `id_materia`: uuid.UUID - o ID da matéria
    
    Retorna o código da matéria se ela existir, e None caso contrário.
    """
    materia = Materia.query.filter_by(id=id_materia).first()
    return materia.codigo if materia else None

def buscar_llm_materia_por_id(id_materia: uuid.UUID) -> str | None:
        """
        Busca o nome da LLM associada a uma matéria pelo ID da matéria.

        :param materia_id: UUID da matéria
        :return: Nome da LLM ou None se não houver associação
        """
        materia = Materia.query.filter_by(id=id_materia).first()
        if not materia:
            return None
        
        if materia.llm:
            return materia.llm.nome  
        
        return None


def getAllSubjects(nome: str = None, codigo: str = None):
     
    query = Materia.query

    if nome: 
          query = query.filter(
               Materia.nome.ilike(f"%{nome}%")
          )

    if codigo:
         query = query.filter(
              Materia.codigo.ilike(f"%{codigo}%")
         )

    return query.order_by(Materia.nome.asc())


def createSubject(nome: str = None, codigo: str = None):
     
    materia = Materia(
         nome=nome,
         codigo=codigo,
         status=StatusMateriaEnum.ATIVO
    )

    db.session.add(materia)
    db.session.flush()

    db.session.commit()
    return materia.to_dict()
