import uuid
from application.config.database import db


class TokenConvite(db.Model):
    __tablename__ = 'token_convite'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = db.Column(db.String(36), nullable=False, unique=True, index=True)
    usuario_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey('usuario.id', ondelete='CASCADE'),
        nullable=False
    )
    used = db.Column(db.Boolean, default=False, nullable=False)

    usuario = db.relationship(
        'Usuario',
        backref=db.backref('tokens_convite', cascade='all, delete-orphan')
    )

    def to_dict(self):
        return {
            'id': str(self.id),
            'token': self.token,
            'usuario_id': str(self.usuario_id),
            'used': self.used
        }