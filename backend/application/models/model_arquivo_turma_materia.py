from application.config.database import db

class ArquivoTurmaMateria(db.Model):
    """
    Relaciona Arquivos com Matérias dentro de Turmas específicas.
    """
    __tablename__ = 'arquivos_turmas_materias'

    arquivo_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('arquivos.id'), nullable=False, primary_key=True)
    turma_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('turmas.id'), nullable=False, primary_key=True)
    materia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('materias.id'), nullable=False, primary_key=True)

    arquivo = db.relationship('Arquivo', back_populates='turmas_materias')
    turma = db.relationship('Turma', back_populates='arquivos')
    materia = db.relationship('Materia', back_populates='arquivos')
