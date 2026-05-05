import sys
from unittest.mock import MagicMock
import uuid
from datetime import datetime 

#Tive que mockar alguns import para poder rodar a função isoladamente
sys.modules["application.config.vector_database"] = MagicMock()
sys.modules["chromadb"] = MagicMock()
sys.modules["ollama"] = MagicMock()
sys.modules["application.socket.socketio"] = MagicMock()

from app import app
from application.models import Chat
from application.socket.Impl.registrar_mensagem import registrar_mensagem
from application.config.database import db
from application.models.model_usuario import Usuario, RoleEnum
from application.models.model_sessao import Sessao

def test_registrar_mensagem():
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
        
        chat = Chat.query.filter_by(id="88e405c6-f81c-48ee-acdf-cc27ac671815").first()

        if not chat:
            chat = Chat(
                aluno_id=aluno_id,
                materia_id=str(uuid.uuid4()),
                nome="teste"
            )
            db.session.add(chat)

        sessao = Sessao.query.filter_by(id="80423d12-440a-480b-b1b4-fa68912d11fa").first()

        if not sessao:
            sessao = Sessao(
                dono_id=usuario.id,
                inicio=datetime.now(),
                fim=datetime.now()
            )
            db.session.add(sessao)

        db.session.commit()

        id_mensagem = registrar_mensagem(id_chat=chat.id, usuario_id=usuario.id, sessao_id=sessao.id, data_de_envio=datetime.now(), conteudo="teste final xd")

        assert id_mensagem is not None

        print("Teste de integração passou")


if __name__ == "__main__":
    test_registrar_mensagem()