from application.config.database import db

class LLM(db.Model):
    __tablename__ = "llm"

    id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    status = db.Column(
        db.Enum('ativada', 'desativada', name='llmstatusenum', native_enum=False),
        nullable=False,
        default='desativada',
        server_default='desativada',
    )

    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto LLM em um dicionário serializável.

        Retorna um dicionário contendo as informações do chat.
        """
        return {
            'id': str(self.id),
            'nome': self.nome,
            'status': self.status,
        }