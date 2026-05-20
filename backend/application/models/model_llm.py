from application.config.database import db

class LLM(db.Model):
    __tablename__ = "llm"

    model_id = db.Column(db.String, primary_key=True)
    
    status = db.Column(
        db.Enum('ativada', 'desativada', name='llmstatusenum', native_enum=False),
        nullable=False,
        default='desativada',
        server_default='desativada',
    )