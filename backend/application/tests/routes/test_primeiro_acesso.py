"""
Testes de integração para o fluxo de criação de senha no primeiro acesso.

Cobre os critérios de aceitação de:
- POST /admin/usuarios/criar
- GET  /auth/invite/validate/<token>
- POST /admin/usuarios/recriar_senha
"""
import sys
from unittest.mock import MagicMock, patch
import pytest

sys.modules["application.config.vector_database"] = MagicMock()
sys.modules["chromadb"] = MagicMock()
sys.modules["ollama"] = MagicMock()
sys.modules["application.socket.socket_instance"] = MagicMock()
sys.modules["application.socket.event_handler"] = MagicMock()

from app import app
from application.auth.jwt_handler import gerar_token


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def admin_headers():
    """JWT de ADMIN — as rotas /usuarios/* passaram a exigir admin autenticado (GAP-02-A)."""
    with app.app_context():
        token = gerar_token("00000000-0000-0000-0000-0000000000ad", "ADMIN")
    return {"Authorization": f"Bearer {token}"}


PAYLOAD_CRIAR = {
    "matricula": "20240099",
    "nome": "Novo Aluno",
    "email": "novo@iesb.edu.br",
}

USUARIO_DICT = {
    "id": "uuid-fake-123",
    "matricula": "20240099",
    "nome": "Novo Aluno",
    "email": "novo@iesb.edu.br",
    "role": "RoleEnum.ALUNO",
    "status": "RoleEnum.ATIVO",
}

TOKEN_FAKE = "token-uuid-fake"


# ---------------------------------------------------------------------------
# POST /admin/usuarios/criar — testes de rota
# ---------------------------------------------------------------------------

class TestCriarUsuario:

    @patch("application.routes.route_admin.enviar_email_convite_async")
    @patch("application.routes.route_admin.criar_usuario")
    @patch("application.routes.route_admin.Usuario")
    def test_retorna_201_em_caso_de_sucesso(self, mock_usuario, mock_criar, mock_email, client, admin_headers):
        """Retorna 201 Created ao criar usuário com dados válidos."""
        mock_usuario.query.filter.return_value.first.return_value = None
        mock_criar.return_value = (USUARIO_DICT, TOKEN_FAKE)

        response = client.post("/admin/usuarios/criar", json=PAYLOAD_CRIAR, headers=admin_headers)

        assert response.status_code == 201

    @patch("application.routes.route_admin.enviar_email_convite_async")
    @patch("application.routes.route_admin.criar_usuario")
    @patch("application.routes.route_admin.Usuario")
    def test_dispara_email_com_dados_e_token_corretos(self, mock_usuario, mock_criar, mock_email, client, admin_headers):
        """Dispara o e-mail de convite com e-mail, nome e token corretos."""
        mock_usuario.query.filter.return_value.first.return_value = None
        mock_criar.return_value = (USUARIO_DICT, TOKEN_FAKE)

        client.post("/admin/usuarios/criar", json=PAYLOAD_CRIAR, headers=admin_headers)

        mock_email.assert_called_once_with(
            PAYLOAD_CRIAR["email"],
            PAYLOAD_CRIAR["nome"],
            TOKEN_FAKE,
        )

    @patch("application.routes.route_admin.enviar_email_convite_async")
    @patch("application.routes.route_admin.criar_usuario")
    @patch("application.routes.route_admin.Usuario")
    def test_nao_dispara_email_para_usuario_via_google(self, mock_usuario, mock_criar, mock_email, client, admin_headers):
        """Não dispara e-mail de convite quando via_google=True."""
        mock_usuario.query.filter.return_value.first.return_value = None
        mock_criar.return_value = (USUARIO_DICT, None)

        client.post("/admin/usuarios/criar", json={**PAYLOAD_CRIAR, "via_google": True}, headers=admin_headers)

        mock_email.assert_not_called()

    @patch("application.routes.route_admin.Usuario")
    def test_email_fora_do_dominio_retorna_400(self, mock_usuario, client, admin_headers):
        """Rejeita e-mail fora do domínio @iesb.edu.br com 400."""
        payload = {**PAYLOAD_CRIAR, "email": "aluno@gmail.com"}

        response = client.post("/admin/usuarios/criar", json=payload, headers=admin_headers)

        assert response.status_code == 400

    @patch("application.routes.route_admin.Usuario")
    def test_usuario_duplicado_retorna_409(self, mock_usuario, client, admin_headers):
        """Retorna 409 quando matrícula ou e-mail já existem no banco."""
        mock_usuario.query.filter.return_value.first.return_value = MagicMock()

        response = client.post("/admin/usuarios/criar", json=PAYLOAD_CRIAR, headers=admin_headers)

        assert response.status_code == 409

    def test_sem_token_retorna_401(self, client):
        """Sem autenticação a criação é bloqueada no backend (GAP-02-A)."""
        response = client.post("/admin/usuarios/criar", json=PAYLOAD_CRIAR)
        assert response.status_code == 401

    def test_perfil_nao_admin_retorna_403(self, client):
        """Usuário autenticado que não é admin não pode criar (GAP-02-A)."""
        with app.app_context():
            token = gerar_token("11111111-1111-1111-1111-111111111111", "PROFESSOR")
        response = client.post(
            "/admin/usuarios/criar", json=PAYLOAD_CRIAR,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403


# ---------------------------------------------------------------------------
# POST /admin/usuarios/criar — testes de serviço
# ---------------------------------------------------------------------------

class TestServiceCriarUsuario:

    @patch("application.services.service_usuario.db")
    @patch("application.services.service_usuario.TokenConvite")
    @patch("application.services.service_usuario.generate_password_hash")
    @patch("application.services.service_usuario.Usuario")
    def test_senha_gerada_com_hash_aplicado(self, mock_usuario_cls, mock_hash, mock_token_cls, mock_db):
        """Cria o usuário com hash aplicado sobre a senha aleatória gerada."""
        from application.services.service_usuario import criar_usuario

        mock_hash.return_value = "senha_hasheada"
        usuario_mock = MagicMock()
        usuario_mock.id = "uuid-fake"
        usuario_mock.to_dict.return_value = USUARIO_DICT
        mock_usuario_cls.return_value = usuario_mock

        criar_usuario("20240099", "Novo Aluno", "novo@iesb.edu.br")

        mock_hash.assert_called_once()
        assert mock_usuario_cls.call_args.kwargs["senha"] == "senha_hasheada"

    @patch("application.services.service_usuario.db")
    @patch("application.services.service_usuario.TokenConvite")
    @patch("application.services.service_usuario.generate_password_hash")
    @patch("application.services.service_usuario.Usuario")
    def test_token_gerado_vinculado_ao_usuario_com_used_false(self, mock_usuario_cls, mock_hash, mock_token_cls, mock_db):
        """Gera token único vinculado ao usuário e marcado como used=False."""
        from application.services.service_usuario import criar_usuario

        usuario_mock = MagicMock()
        usuario_mock.id = "uuid-fake"
        usuario_mock.to_dict.return_value = USUARIO_DICT
        mock_usuario_cls.return_value = usuario_mock

        _, token_str = criar_usuario("20240099", "Novo Aluno", "novo@iesb.edu.br")

        assert token_str is not None
        assert mock_token_cls.call_args.kwargs["used"] is False
        assert mock_token_cls.call_args.kwargs["usuario_id"] == "uuid-fake"


# ---------------------------------------------------------------------------
# GET /auth/invite/validate/<token> — testes de rota
# ---------------------------------------------------------------------------

class TestValidarTokenConvite:

    @patch("application.routes.route_auth.validar_token_convite")
    def test_token_valido_retorna_200_com_dados_do_usuario(self, mock_validar, client):
        """Retorna 200 OK com nome e e-mail do usuário quando token existe e used=False."""
        mock_validar.return_value = (
            {"nome": "Novo Aluno", "email": "novo@iesb.edu.br"},
            "valido",
        )

        response = client.get(f"/auth/invite/validate/{TOKEN_FAKE}")
        dados = response.get_json()

        assert response.status_code == 200
        assert "nome" in dados
        assert "email" in dados

    @patch("application.routes.route_auth.validar_token_convite")
    def test_token_ja_utilizado_retorna_410_com_orientacao(self, mock_validar, client):
        """Retorna 410 Gone com orientação para 'Esqueci minha senha' quando token já foi usado."""
        mock_validar.return_value = (None, "utilizado_ou_inexistente")

        response = client.get(f"/auth/invite/validate/{TOKEN_FAKE}")
        dados = response.get_json()

        assert response.status_code == 410
        assert "Esqueci minha senha" in dados.get("orientacao", "")

    @patch("application.routes.route_auth.validar_token_convite")
    def test_token_inexistente_retorna_410_com_orientacao(self, mock_validar, client):
        """Retorna 410 Gone com orientação para 'Esqueci minha senha' quando token não existe."""
        mock_validar.return_value = (None, "utilizado_ou_inexistente")

        response = client.get("/auth/invite/validate/token-inexistente")
        dados = response.get_json()

        assert response.status_code == 410
        assert "Esqueci minha senha" in dados.get("orientacao", "")


# ---------------------------------------------------------------------------
# POST /admin/usuarios/recriar_senha — testes de rota
# ---------------------------------------------------------------------------

class TestRecriarSenha:

    URL = "/admin/usuarios/recriar_senha"

    def _payload(self, token=TOKEN_FAKE, password="Senha@Valida1", confirmation=None):
        return {
            "token": token,
            "password": password,
            "passwordConfirmation": confirmation if confirmation is not None else password,
        }

    def test_senhas_diferentes_retornam_400(self, client):
        """Rejeita com 400 quando password e passwordConfirmation não coincidem."""
        response = client.post(self.URL, json=self._payload(
            password="Senha@Valida1",
            confirmation="Diferente@2",
        ))

        assert response.status_code == 400
        assert "não coincidem" in response.get_json().get("error", "")

    @pytest.mark.parametrize("senha_fraca,trecho_esperado", [
        ("Ab1",           "mínimo"),
        ("semaiuscula1",  "maiúscula"),
        ("SEMMINUSCULA1", "minúscula"),
        ("SemNumero",     "número"),
    ])
    def test_senha_fraca_retorna_400_com_mensagem_explicativa(self, client, senha_fraca, trecho_esperado):
        """Rejeita senhas que não atendam aos critérios mínimos com 400 e mensagem explicativa."""
        response = client.post(self.URL, json=self._payload(
            password=senha_fraca,
            confirmation=senha_fraca,
        ))

        assert response.status_code == 400
        assert trecho_esperado in response.get_json().get("error", "")

    @patch("application.routes.route_admin.gerar_token")
    @patch("application.routes.route_admin.definir_senha_primeiro_acesso")
    def test_sucesso_retorna_200(self, mock_definir, mock_jwt, client):
        """Retorna 200 OK após definir a senha com sucesso."""
        mock_definir.return_value = USUARIO_DICT
        mock_jwt.return_value = "jwt-fake"

        response = client.post(self.URL, json=self._payload())

        assert response.status_code == 200

    @patch("application.routes.route_admin.gerar_token")
    @patch("application.routes.route_admin.definir_senha_primeiro_acesso")
    def test_sucesso_inicia_sessao_com_cookie_jwt(self, mock_definir, mock_jwt, client):
        """Retorna cookie JWT de sessão após definir a senha com sucesso."""
        mock_definir.return_value = USUARIO_DICT
        mock_jwt.return_value = "jwt-fake"

        response = client.post(self.URL, json=self._payload())

        assert "token" in response.headers.get("Set-Cookie", "")

    @patch("application.routes.route_admin.definir_senha_primeiro_acesso")
    def test_token_invalido_ou_ja_usado_retorna_410(self, mock_definir, client):
        """Retorna 410 Gone quando o token é inválido ou já foi utilizado."""
        mock_definir.return_value = None

        response = client.post(self.URL, json=self._payload())

        assert response.status_code == 410


# ---------------------------------------------------------------------------
# POST /admin/usuarios/recriar_senha — testes de serviço
# ---------------------------------------------------------------------------

class TestServiceDefinirSenha:

    @patch("application.services.service_usuario.db")
    @patch("application.services.service_usuario.generate_password_hash")
    @patch("application.services.service_usuario.TokenConvite")
    def test_senha_sobrescrita_com_hash(self, mock_token_cls, mock_hash, mock_db):
        """Sobrescreve a senha aleatória com a nova senha hasheada."""
        from application.services.service_usuario import definir_senha_primeiro_acesso

        mock_hash.return_value = "nova_senha_hasheada"
        usuario_mock = MagicMock()
        usuario_mock.to_dict.return_value = USUARIO_DICT
        token_mock = MagicMock()
        token_mock.used = False
        token_mock.usuario = usuario_mock
        mock_token_cls.query.filter_by.return_value.first.return_value = token_mock

        definir_senha_primeiro_acesso(TOKEN_FAKE, "NovaSenha@99")

        mock_hash.assert_called_once_with("NovaSenha@99")
        assert usuario_mock.senha == "nova_senha_hasheada"

    @patch("application.services.service_usuario.db")
    @patch("application.services.service_usuario.generate_password_hash")
    @patch("application.services.service_usuario.TokenConvite")
    def test_token_marcado_como_used_true_apos_uso(self, mock_token_cls, mock_hash, mock_db):
        """Marca o token como used=True após uso bem-sucedido."""
        from application.services.service_usuario import definir_senha_primeiro_acesso

        usuario_mock = MagicMock()
        usuario_mock.to_dict.return_value = USUARIO_DICT
        token_mock = MagicMock()
        token_mock.used = False
        token_mock.usuario = usuario_mock
        mock_token_cls.query.filter_by.return_value.first.return_value = token_mock

        definir_senha_primeiro_acesso(TOKEN_FAKE, "NovaSenha@99")

        assert token_mock.used is True

    @patch("application.services.service_usuario.db")
    @patch("application.services.service_usuario.TokenConvite")
    def test_token_reutilizado_retorna_none(self, mock_token_cls, mock_db):
        """Token não pode ser reutilizado — retorna None quando used=True."""
        from application.services.service_usuario import definir_senha_primeiro_acesso

        token_mock = MagicMock()
        token_mock.used = True
        mock_token_cls.query.filter_by.return_value.first.return_value = token_mock

        resultado = definir_senha_primeiro_acesso(TOKEN_FAKE, "NovaSenha@99")

        assert resultado is None