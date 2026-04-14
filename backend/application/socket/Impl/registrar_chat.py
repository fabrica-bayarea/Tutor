from application.models.model_chat import Chat
from application.config.database import db

def registrar_chat(id_usuario, id_materia, primeiro_titulo): 
    try: 
        titulo = primeiro_titulo.strip().replace("\n", " ")
        titulo = " ".join(titulo.split())
        titulo = titulo[:50]

        if not titulo: 
            titulo = "Novo chat"

        novo_chat = Chat(
            aluno_id =id_usuario,
            materia_id=id_materia,
            nome=titulo
        )

        db.session.add(novo_chat)
        db.session.commit()

        return novo_chat.id

    except Exception as e:
        db.session.rollback()
        print(f"[Error] erro ao registrar chat: {e}")
        raise
