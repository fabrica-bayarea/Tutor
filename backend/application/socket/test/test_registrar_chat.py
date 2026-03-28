import sys
from unittest.mock import MagicMock
import uuid

#Tive que mockar alguns import para poder rodar a função isoladamente
sys.modules["application.config.vector_database"] = MagicMock()
sys.modules["chromadb"] = MagicMock()
sys.modules["ollama"] = MagicMock()
sys.modules["application.socket.socketio"] = MagicMock()

from app import app
from application.models import Chat
from application.socket.Impl.event_handlers import registrar_chat
from application.config.database import db
from application.models.model_usuario import Usuario, RoleEnum
from application.models.model_materia import Materia

def test_registrar_chat():
    with app.app_context():

        aluno_id = uuid.uuid4()
        usuario = Usuario.query.filter_by(matricula="20260001").first()

        if not usuario:
            usuario = Usuario(
            id=aluno_id,
            matricula="20260001",
            nome="Usuário Teste",
            email=f"teste_{aluno_id}@email.com",
            senha="123456",
            role=RoleEnum.ALUNO
        )
            db.session.add(usuario)


        materia = Materia.query.filter_by(codigo="MAT001").first()

        if not materia:
            materia = Materia(
            codigo="MAT001",
            nome="Matéria Teste"
            )
            db.session.add(materia)

        db.session.commit()


        id_chat = registrar_chat(id_usuario=usuario.id ,id_materia=materia.id, primeiro_titulo="Chat de teste")

        assert id_chat is not None

        print("Teste de integração passou")

        chat = db.session.get(Chat, id_chat)
        if chat:
            db.session.delete(chat)
            db.session.commit()

if __name__ == "__main__":
    test_registrar_chat()


