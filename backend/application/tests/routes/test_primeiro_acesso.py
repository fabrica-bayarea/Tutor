"""
Testes de integração para o fluxo de criação de senha no primeiro acesso.

Cobre os critérios de aceitação de:
- POST /admin/usuarios/criar
- GET  /auth/invite/validate/<token>
- POST /admin/usuarios/recriar_senha
"""
import uuid
import pytest
from unittest.mock import patch
from werkzeug.security import generate_password_hash, check_password_hash

from application import create_app  # ajuste o import se necessário
from application.config.database import db
from application.models.model_usuario import Usuario, RoleEnum
from application.models.model_token_convite import TokenConvite


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope='session')
def app():
    """Cria a aplicação Flask em modo de teste com banco SQLite em memória."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'chave-de-teste',
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(autouse=True)
def limpar_banco(app):
    """Limpa as tabelas relevantes antes de cada teste para garantir isolamento."""
    with app.app_context():
        yield
        db.session.rollback()
        TokenConvite.query.delete()
        Usuario.query.delete()
        db.session.commit()


@pytest.fixture
def client(app):
    """Cliente HTTP de teste do Flask."""
    return app.test_client()


@pytest.fixture
def usuario_base(app):
    """Cria e persiste um usuário padrão para uso nos testes."""
    with app.app_context():
        usuario = Usuario(
            matricula='20240001',
            nome='Usuário Teste',
            email='teste@iesb.edu.br',
            senha=generate_password_hash('SenhaAleatoria123'),
            role=RoleEnum.ALUNO,
            status=RoleEnum.ATIVO,
        )
        db.session.add(usuario)
        db.session.commit()
        return str(usuario.id)


@pytest.fixture
def token_valido(app, usuario_base):
    """Cria um token de convite válido (used=False) vinculado ao usuário base."""
    with app.app_context():
        token_str = str(uuid.uuid4())
        token = TokenConvite(
            token=token_str,
            usuario_id=uuid.UUID(usuario_base),
            used=False,
        )
        db.session.add(token)
        db.session.commit()
        return token_str


@pytest.fixture
def token_usado(app, usuario_base):
    """Cria um token de convite já utilizado (used=True) vinculado ao usuário base."""
    with app.app_context():
        token_str = str(uuid.uuid4())
        token = TokenConvite(
            token=token_str,
            usuario_id=uuid.UUID(usuario_base),
            used=True,
        )
        db.session.add(token)
        db.session.commit()
        return token_str


# ---------------------------------------------------------------------------
# POST /admin/usuarios/criar
# ---------------------------------------------------------------------------

class TestCriarUsuario:
    """Critérios de aceitação — POST /admin/usuarios/criar"""

    PAYLOAD = {
        'matricula': '20240099',
        'nome': 'Novo Aluno',
        'email': 'novo@iesb.edu.br',
    }

    @patch('application.routes.route_admin.enviar_email_convite')
    def test_retorna_201_em_caso_de_sucesso(self, mock_email, client):
        """Retorna 201 Created ao criar usuário com dados válidos."""
        resposta = client.post('/admin/usuarios/criar', json=self.PAYLOAD)

        assert resposta.status_code == 201

    @patch('application.routes.route_admin.enviar_email_convite')
    def test_senha_persistida_com_hash(self, mock_email, app, client):
        """Cria o usuário com senha hasheada — nunca em texto puro."""
        client.post('/admin/usuarios/criar', json=self.PAYLOAD)

        with app.app_context():
            usuario = Usuario.query.filter_by(email=self.PAYLOAD['email']).first()

        assert usuario is not None
        # A senha não pode ser uma string simples legível
        assert usuario.senha != self.PAYLOAD.get('senha', '')
        # Deve ser reconhecida como hash pelo werkzeug
        assert usuario.senha.startswith(('pbkdf2:', 'scrypt:', '$2b$'))

    @patch('application.routes.route_admin.enviar_email_convite')
    def test_token_gerado_com_used_false(self, mock_email, app, client):
        """Gera um token único vinculado ao usuário e marcado como used=False."""
        client.post('/admin/usuarios/criar', json=self.PAYLOAD)

        with app.app_context():
            usuario = Usuario.query.filter_by(email=self.PAYLOAD['email']).first()
            token = TokenConvite.query.filter_by(usuario_id=usuario.id).first()

        assert token is not None
        assert token.used is False
        assert token.usuario_id == usuario.id

    @patch('application.routes.route_admin.enviar_email_convite')
    def test_email_convite_disparado_ao_final_do_cadastro(self, mock_email, client):
        """Dispara o e-mail de convite com o link de redefinição ao criar o usuário."""
        client.post('/admin/usuarios/criar', json=self.PAYLOAD)

        mock_email.assert_called_once()
        args = mock_email.call_args[0]
        assert args[0] == self.PAYLOAD['email']   # destinatário correto
        assert args[1] == self.PAYLOAD['nome']     # nome correto

    def test_nao_dispara_email_para_usuario_via_google(self, client):
        """Não dispara o fluxo de convite para usuários cadastrados via Google."""
        payload = {**self.PAYLOAD, 'via_google': True}

        with patch('application.routes.route_admin.enviar_email_convite') as mock_email:
            client.post('/admin/usuarios/criar', json=payload)
            mock_email.assert_not_called()


# ---------------------------------------------------------------------------
# GET /auth/invite/validate/<token>
# ---------------------------------------------------------------------------

class TestValidarTokenConvite:
    """Critérios de aceitação — GET /auth/invite/validate/<token>"""

    def test_token_valido_retorna_200_com_dados_do_usuario(self, client, token_valido):
        """Retorna 200 OK com dados básicos do usuário quando token existe e used=False."""
        resposta = client.get(f'/auth/invite/validate/{token_valido}')
        dados = resposta.get_json()

        assert resposta.status_code == 200
        assert 'nome' in dados
        assert 'email' in dados

    def test_token_ja_utilizado_retorna_410(self, client, token_usado):
        """Retorna 410 Gone quando o token já foi utilizado (used=True)."""
        resposta = client.get(f'/auth/invite/validate/{token_usado}')
        dados = resposta.get_json()

        assert resposta.status_code == 410
        assert 'orientacao' in dados
        assert 'Esqueci minha senha' in dados['orientacao']

    def test_token_inexistente_retorna_410(self, client):
        """Retorna 410 Gone quando o token não existe no banco."""
        token_falso = str(uuid.uuid4())
        resposta = client.get(f'/auth/invite/validate/{token_falso}')
        dados = resposta.get_json()

        assert resposta.status_code == 410
        assert 'orientacao' in dados
        assert 'Esqueci minha senha' in dados['orientacao']


# ---------------------------------------------------------------------------
# POST /admin/usuarios/recriar_senha
# ---------------------------------------------------------------------------

class TestRecriarSenha:
    """Critérios de aceitação — POST /admin/usuarios/recriar_senha"""

    URL = '/admin/usuarios/recriar_senha'

    def _payload(self, token, password='Senha@Valida1', confirmation=None):
        return {
            'token': token,
            'password': password,
            'passwordConfirmation': confirmation if confirmation is not None else password,
        }

    # --- Validação de confirmação de senha ---

    def test_senhas_diferentes_retornam_400(self, client, token_valido):
        """Rejeita com 400 quando password e passwordConfirmation não coincidem."""
        payload = self._payload(token_valido, password='Senha@Valida1', confirmation='Diferente@2')
        resposta = client.post(self.URL, json=payload)

        assert resposta.status_code == 400
        assert 'não coincidem' in resposta.get_json().get('error', '')

    # --- Validação de força da senha ---

    @pytest.mark.parametrize('senha_fraca,trecho_esperado', [
        ('Ab1',         'mínimo'),       # muito curta
        ('semaiuscula1','maiúscula'),    # sem maiúscula
        ('SEMMINUSCULA1','minúscula'),   # sem minúscula
        ('SemNumero',  'número'),        # sem número
    ])
    def test_senha_fraca_retorna_400_com_mensagem(self, client, token_valido, senha_fraca, trecho_esperado):
        """Rejeita senhas fracas com 400 e mensagem explicativa adequada."""
        payload = self._payload(token_valido, password=senha_fraca, confirmation=senha_fraca)
        resposta = client.post(self.URL, json=payload)
        dados = resposta.get_json()

        assert resposta.status_code == 400
        assert trecho_esperado in dados.get('error', '')

    # --- Persistência e segurança ---

    def test_senha_sobrescrita_com_hash(self, app, client, token_valido, usuario_base):
        """Sobrescreve a senha aleatória com a nova senha aplicando hash."""
        nova_senha = 'NovaSenha@99'
        client.post(self.URL, json=self._payload(token_valido, password=nova_senha))

        with app.app_context():
            usuario = Usuario.query.get(uuid.UUID(usuario_base))

        assert check_password_hash(usuario.senha, nova_senha)

    def test_token_marcado_como_used_true(self, app, client, token_valido):
        """Marca o token como used=True após uso bem-sucedido."""
        client.post(self.URL, json=self._payload(token_valido))

        with app.app_context():
            token = TokenConvite.query.filter_by(token=token_valido).first()

        assert token.used is True

    def test_retorna_200_com_cookie_de_sessao(self, client, token_valido):
        """Retorna 200 OK e define o cookie de sessão JWT após criar a senha."""
        resposta = client.post(self.URL, json=self._payload(token_valido))

        assert resposta.status_code == 200
        assert 'token' in resposta.headers.get('Set-Cookie', '')

    def test_token_nao_pode_ser_reutilizado(self, client, token_valido):
        """Token não pode ser reutilizado após uso bem-sucedido."""
        payload = self._payload(token_valido)

        primeira = client.post(self.URL, json=payload)
        segunda = client.post(self.URL, json=payload)

        assert primeira.status_code == 200
        assert segunda.status_code == 410