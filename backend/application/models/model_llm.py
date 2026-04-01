from application.config.database import db

class LLM(db.Model):
    __tablename__ = "llm"

    model_id = db.Column(db.String, primary_key=True)