from application.config.database import db
import uuid
from sqlalchemy.sql import func

class Sessao(db.Model):
    __tablename__ = 'sessao'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dono_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('usuario.id'), nullable=False)
    inicio = db.Column(db.DateTime, nullable=False, server_default=func.now())
    fim = db.Column(db.DateTime, nullable=False, server_default=func.now())

    usuario = db.relationship("Usuario")

    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto Turma em um dicionário serializável.

        Retorna um dicionário contendo as informações da turma.
        """
        return {
            'id': str(self.id),
            'dono_id': str(self.dono_id),
            'inicio': self.inicio.strftime('%d/%m/%Y'),
            'fim': self.fim.strftime('%d/%m/%Y')
        }
