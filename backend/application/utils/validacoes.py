from application.config import db
from application.models import *
import uuid

def validar_aluno(aluno_id: uuid.UUID) -> bool:
    aluno = db.session.query(Aluno).filter_by(id=aluno_id).first()
    return aluno is not None

def validar_professor(professor_id: uuid.UUID) -> bool:
    professor = db.session.query(Professor).filter_by(id=professor_id).first()
    return professor is not None

def validar_turma(turma_id: uuid.UUID) -> bool:
    turma = db.session.query(Turma).filter_by(id=turma_id).first()
    return turma is not None

def validar_materia(materia_id: uuid.UUID) -> bool:
    materia = db.session.query(Materia).filter_by(id=materia_id).first()
    return materia is not None

def validar_arquivo(arquivo_id: uuid.UUID) -> bool:
    arquivo = db.session.query(Arquivo).filter_by(id=arquivo_id).first()
    return arquivo is not None

def validar_aluno_turma(aluno_id: uuid.UUID, turma_id: uuid.UUID) -> bool:
    aluno_turma = db.session.query(AlunoTurma).filter_by(aluno_id=aluno_id, turma_id=turma_id).first()
    return aluno_turma is not None

def validar_turma_materia(turma_id: uuid.UUID, materia_id: uuid.UUID) -> bool:
    turma_materia = db.session.query(TurmaMateria).filter_by(turma_id=turma_id, materia_id=materia_id).first()
    return turma_materia is not None

def validar_professor_turma_materia(professor_id: uuid.UUID, turma_id: uuid.UUID, materia_id: uuid.UUID) -> bool:
    professor_turma_materia = db.session.query(ProfessorTurmaMateria).filter_by(professor_id=professor_id, turma_id=turma_id, materia_id=materia_id).first()
    return professor_turma_materia is not None

def validar_arquivo_turma_materia(arquivo_id: uuid.UUID, turma_id: uuid.UUID, materia_id: uuid.UUID) -> bool:
    arquivo_turma_materia = db.session.query(ArquivoTurmaMateria).filter_by(arquivo_id=arquivo_id, turma_id=turma_id, materia_id=materia_id).first()
    return arquivo_turma_materia is not None

def validar_chat(chat_id: uuid.UUID) -> bool:
    chat = db.session.query(Chat).filter_by(id=chat_id).first()
    return chat is not None

def validar_mensagem(mensagem_id: uuid.UUID) -> bool:
    mensagem = db.session.query(Mensagem).filter_by(id=mensagem_id).first()
    return mensagem is not None
