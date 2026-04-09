
from application.socket.Impl.llm_providers.gpt_provider import gpt_provider
from application.socket.Impl.llm_providers.claude_provider import claude_provider
from application.socket.Impl.llm_providers.gemini_provider import gemini_provider
from application.socket.Impl.llm_providers.local_provider import local_provider


def obter_provider(id_llm):
    
    if id_llm.startswith("gpt"):
        return gpt_provider
    elif id_llm.startswith("claude"):
        return claude_provider
    elif id_llm.startswith("gemini"):
        return gemini_provider
    elif id_llm == "local":
        return local_provider
    else:
        return ValueError(f"LLM não suportada: {id_llm}") 