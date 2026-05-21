import uuid
from application.models import Materia, Turma
from application.models.model_materia import StatusMateriaEnum
from application.models.model_turma import StatusTurmaEnum
from application.config.database import db
from application.models.model_turma_materia import TurmaMateria

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


def updateSubject(id: uuid.uuid4, nome_novo: str = None, codigo_novo: str = None, status_novo: str = None):
    materia = Materia.query.get(id)

    if not materia:
          return None
    
    materia.nome = nome_novo
    materia.codigo = codigo_novo
    materia.status = status_novo

    db.session.commit()

    return materia.to_dict()
    


def deleteSubject(id: uuid.uuid4):
    materia = Materia.query.get(id)

    if not materia:
        return None, {'materia_nao_encontrada'}

    if materia.llm_id:
        return None, {'materia_nao_pode_ser_desativada'}

    turma_ativa = (
        db.session.query(TurmaMateria)
        .join(Turma)
        .filter(
            TurmaMateria.materia_id == id,
            Turma.status == StatusTurmaEnum.ATIVO
        )
        .first()
    )

    if turma_ativa:
        return None, {'materia_vinculada_turma_ativa'}

    materia.status = StatusMateriaEnum.INATIVO
    db.session.commit()

    return materia, None

