from application.config.database import db
from application.models.model_mensagem import Mensagem


def registrar_mensagem(id_chat, usuario_id, sessao_id, data_de_envio, conteudo):
    try:
        if not conteudo:
            print(f"[Warning] problema ao registrar mesnagem, conteudo vazio")
            return
        
        nova_mensagem = Mensagem(
            chat_id=id_chat,
            sessao_id=sessao_id,
            sender_id=usuario_id,
            conteudo=conteudo,
            data_envio=data_de_envio
        )

        db.session.add(nova_mensagem)
        db.session.commit()

        return nova_mensagem.id

    except Exception as e:
        db.session.rollback()
        print(f"[Error] erro ao persistir mensagem: {e}")
        return None