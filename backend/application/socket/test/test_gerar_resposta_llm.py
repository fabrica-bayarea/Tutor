import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from application.socket.Impl.gerar_resposta_llm import gerar_resposta_llm

async def test_gerar_resposta_llm_mcp():

    socket_mock = MagicMock()

    mock_resultado = [MagicMock(text="Olá mundo")]

    mock_mcp = MagicMock()
    mock_mcp.connect_to_server = AsyncMock()
    mock_mcp.call_tool = AsyncMock(return_value=mock_resultado)

    with patch(
        "application.socket.Impl.gerar_resposta_llm.MCPClientManager",
        return_value=mock_mcp
    ), patch(
        "application.socket.Impl.gerar_resposta_llm.registrar_mensagem",
        return_value=None
    ):
        await gerar_resposta_llm(
            prompt_completo=[{"role": "user", "content": "oi"}],
            id_llm="gpt-4",
            socket=socket_mock,
            id_mensagem="123",
            id_chat="chat1",
            sessao_id="sessao1"
        )

    calls = socket_mock.emit.call_args_list

    assert any("mensagem_completa" in str(call) for call in calls)

    print("Teste MCP passou!")

print("Rodando teste...")

if __name__ == "__main__":
    asyncio.run(test_gerar_resposta_llm_mcp())