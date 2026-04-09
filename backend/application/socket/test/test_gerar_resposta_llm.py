import asyncio
import sys
from unittest.mock import AsyncMock, MagicMock, patch

sys.modules["application.socket.Impl.registrar_mensagem"] = MagicMock()

from application.socket.Impl.gerar_resposta_llm import gerar_resposta_llm

async def test_gerar_resposta_llm_gpt():

    socket_mock = MagicMock()


    async def mock_stream(client, prompt, model):
        yield "Olá "
        yield "mundo"

    mock_provider = MagicMock(return_value=mock_stream)

    with patch(
        "application.socket.Impl.gerar_resposta_llm.obter_provider",
        return_value=mock_stream
    ), patch(
        "application.socket.Impl.gerar_resposta_llm.obter_provedor_llm",
        return_value=MagicMock()
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

    assert any("chunk_mensagem" in str(call) for call in calls)
    assert any("mensagem_completa" in str(call) for call in calls)

    print("Teste GPT streaming passou!")

print("Rodando teste...")

if __name__ == "__main__":
    asyncio.run(test_gerar_resposta_llm_gpt())