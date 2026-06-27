from application.models import AlunoTurma, TurmaMateria, Turma
import uuid


def buscar_turmas_user(user_id: uuid.UUID) -> list[dict]:
    aluno_turmas = AlunoTurma.query.filter_by(aluno_id=user_id).all()

    if not aluno_turmas:
        return None

    turmas = [at.turma.to_dict() for at in aluno_turmas]

    return turmas


def buscar_materias_user(user_id: uuid.UUID) -> list[dict]:
    aluno_turmas = AlunoTurma.query.filter_by(aluno_id=user_id).all()

    if not aluno_turmas:
        return None

    materias_dict = {}

    for at in aluno_turmas:
        turma = at.turma
        for tm in turma.materias:
            materia = tm.materia
            materias_dict[materia.id] = {
                "id": str(materia.id),
                "nome": materia.nome
            }

    return list(materias_dict.values()) if materias_dict else None
