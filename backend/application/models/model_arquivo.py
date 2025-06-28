from application.config.database import db
import uuid
from datetime import datetime

class Arquivo(db.Model):
    __tablename__ = 'arquivos'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = db.Column(db.String(255), nullable=False)
    professor_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('professores.id'), nullable=False)
    data_upload = db.Column(db.DateTime, nullable=False, default=datetime.now)

    turmas_materias = db.relationship('ArquivoTurmaMateria', back_populates='arquivo')

    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto Arquivo em um dicionário serializável.

        Retorna um dicionário contendo as informações do arquivo.
        """
        return {
            'id': str(self.id),
            'titulo': self.titulo,
            'professor_id': str(self.professor_id),
            'data_upload': self.data_upload.strftime('%d/%m/%Y %H:%M:%S')
        }
