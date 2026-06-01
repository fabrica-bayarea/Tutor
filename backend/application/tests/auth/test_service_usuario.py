"""
Testes unitários do service de usuários.

DB mockado (sem Postgres): exercitam a lógica de filtros/conversões e os fluxos
de ativação/desativação/alteração sem tocar em banco real.
"""
import sys
from unittest.mock import MagicMock, patch

sys.modules.setdefault("chromadb", MagicMock())
sys.modules.setdefault("ollama", MagicMock())
sys.modules.setdefault("application.config.vector_database", MagicMock())

import pytest
from application.models.model_usuario import RoleEnum, StatusEnum
import application.services.service_usuario as svc


# ---------------------------------------------------------------------------
# buscar_alunos_por_filtro — busca única, join de turma e conversão de enums
# ---------------------------------------------------------------------------

@patch("application.services.service_usuario.AlunoTurma")
@patch("application.services.service_usuario.db")
@patch("application.services.service_usuario.Usuario")
def test_buscar_alunos_por_filtro_aplica_todos_os_filtros(mock_usuario, mock_db, mock_aluno_turma):
    q = MagicMock()
    mock_usuario.query = q
    q.join.return_value = q
    q.filter.return_value = q
    q.order_by.return_value = "QUERY_FINAL"

    resultado = svc.buscar_alunos_por_filtro(
        nome="ana", matricula="2024", turma="T1",
        role="ALUNO", status="ATIVO", busca="maria",
    )

    assert resultado == "QUERY_FINAL"
    q.join.assert_called()          # filtro de turma
    assert q.filter.called          # busca única + nome + matricula + role + status
    q.order_by.assert_called_once()


@patch("application.services.service_usuario.db")
@patch("application.services.service_usuario.Usuario")
def test_buscar_alunos_por_filtro_role_status_invalidos_sao_ignorados(mock_usuario, mock_db):
    q = MagicMock()
    mock_usuario.query = q
    q.filter.return_value = q
    q.order_by.return_value = q
    # role/status que não existem no enum não devem gerar filtro nem quebrar
    svc.buscar_alunos_por_filtro(role="INEXISTENTE", status="NAO_EXISTE")
    q.order_by.assert_called_once()


# ---------------------------------------------------------------------------
# desativar / reativar / alterar
# ---------------------------------------------------------------------------

@patch("application.services.service_usuario.db")
@patch("application.services.service_usuario.Usuario")
def test_desativar_aluno_define_inativo_e_commita(mock_usuario, mock_db):
    aluno = MagicMock()
    mock_usuario.query.get.return_value = aluno
    resultado = svc.desativar_aluno("id-1")
    assert aluno.status == StatusEnum.INATIVO
    mock_db.session.commit.assert_called_once()
    assert resultado is aluno


@patch("application.services.service_usuario.Usuario")
def test_desativar_aluno_inexistente_retorna_none(mock_usuario):
    mock_usuario.query.get.return_value = None
    assert svc.desativar_aluno("id-x") is None


@patch("application.services.service_usuario.db")
@patch("application.services.service_usuario.Usuario")
def test_reativar_aluno(mock_usuario, mock_db):
    aluno = MagicMock()
    mock_usuario.query.get.return_value = aluno
    svc.reativar_aluno("id-1")
    assert aluno.status == StatusEnum.ATIVO
    mock_db.session.commit.assert_called_once()


@patch("application.services.service_usuario.Usuario")
def test_reativar_aluno_inexistente_retorna_none(mock_usuario):
    mock_usuario.query.get.return_value = None
    assert svc.reativar_aluno("id-x") is None


@patch("application.services.service_usuario.db")
@patch("application.services.service_usuario.Usuario")
def test_alterar_aluno_por_id_atualiza_campos(mock_usuario, mock_db):
    aluno = MagicMock()
    mock_usuario.query.get.return_value = aluno
    svc.alterar_aluno_por_id("id-1", "2025", "Novo Nome", "n@iesb.edu.br", "ATIVO", "PROFESSOR")
    assert aluno.matricula == "2025"
    assert aluno.nome == "Novo Nome"
    mock_db.session.commit.assert_called_once()


@patch("application.services.service_usuario.Usuario")
def test_alterar_aluno_por_id_inexistente_retorna_none(mock_usuario):
    mock_usuario.query.get.return_value = None
    assert svc.alterar_aluno_por_id("x", "a", "b", "c", "d", "e") is None


# ---------------------------------------------------------------------------
# busca / login / token de convite / força de senha
# ---------------------------------------------------------------------------

@patch("application.services.service_usuario.Usuario")
def test_buscar_aluno_por_id(mock_usuario):
    aluno = MagicMock()
    aluno.to_dict.return_value = {"id": "1"}
    mock_usuario.query.get.return_value = aluno
    assert svc.buscar_aluno(aluno_id="1") == {"id": "1"}


@patch("application.services.service_usuario.db")
@patch("application.services.service_usuario.Usuario")
def test_buscar_aluno_por_filtros(mock_usuario, mock_db):
    aluno = MagicMock()
    aluno.to_dict.return_value = {"email": "a@b.com"}
    mock_usuario.query.filter.return_value.first.return_value = aluno
    assert svc.buscar_aluno(email="a@b.com") == {"email": "a@b.com"}


@patch("application.services.service_usuario.Usuario")
def test_buscar_aluno_sem_filtros_retorna_none(mock_usuario):
    assert svc.buscar_aluno() is None


@patch("application.services.service_usuario.check_password_hash", return_value=True)
@patch("application.services.service_usuario.Usuario")
def test_logar_aluno_sucesso(mock_usuario, _mock_check):
    aluno = MagicMock()
    aluno.to_dict.return_value = {"matricula": "2024"}
    mock_usuario.query.filter_by.return_value.first.return_value = aluno
    assert svc.logar_aluno("2024", "senha") == {"matricula": "2024"}


@patch("application.services.service_usuario.Usuario")
def test_logar_aluno_inexistente(mock_usuario):
    mock_usuario.query.filter_by.return_value.first.return_value = None
    assert svc.logar_aluno("000", "x") is None


@patch("application.services.service_usuario.TokenConvite")
def test_validar_token_convite_invalido(mock_token):
    mock_token.query.filter_by.return_value.first.return_value = None
    dados, status = svc.validar_token_convite("tok")
    assert dados is None and status == "utilizado_ou_inexistente"


@patch("application.services.service_usuario.TokenConvite")
def test_validar_token_convite_valido(mock_token):
    registro = MagicMock(used=False)
    registro.usuario = MagicMock(nome="Ana", email="ana@iesb.edu.br")
    mock_token.query.filter_by.return_value.first.return_value = registro
    dados, status = svc.validar_token_convite("tok")
    assert status == "valido" and dados["nome"] == "Ana"


@patch("application.services.service_usuario.db")
@patch("application.services.service_usuario.generate_password_hash", return_value="hash")
@patch("application.services.service_usuario.TokenConvite")
def test_definir_senha_primeiro_acesso_sucesso(mock_token, _mock_hash, mock_db):
    registro = MagicMock(used=False)
    usuario = MagicMock()
    usuario.to_dict.return_value = {"id": "1"}
    registro.usuario = usuario
    mock_token.query.filter_by.return_value.first.return_value = registro
    resultado = svc.definir_senha_primeiro_acesso("tok", "Senha123")
    assert resultado == {"id": "1"}
    assert registro.used is True
    mock_db.session.commit.assert_called_once()


def test_definir_senha_primeiro_acesso_senha_fraca():
    assert svc.definir_senha_primeiro_acesso("tok", "fraca") is None


@patch("application.services.service_usuario.TokenConvite")
def test_definir_senha_primeiro_acesso_token_invalido(mock_token):
    mock_token.query.filter_by.return_value.first.return_value = None
    assert svc.definir_senha_primeiro_acesso("tok", "Senha123") is None


@pytest.mark.parametrize("senha,ok", [
    ("Senha123", True),
    ("curta1A", False),       # < 8
    ("semmaiuscula1", False),
    ("SEMMINUSCULA1", False),
    ("SemNumeroAa", False),
])
def test_validar_forca_senha(senha, ok):
    erro = svc._validar_forca_senha(senha)
    assert (erro is None) == ok


@patch("application.services.service_usuario.Usuario")
def test_buscar_professor_com_filtros(mock_usuario):
    q = MagicMock()
    mock_usuario.query.filter.return_value = q
    q.filter.return_value = q
    assert svc.buscar_professor(nome="X", matricula="1") is not None
