# from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
# from mistral_common.protocol.instruct.messages import UserMessage, AssistantMessage
# from mistral_common.protocol.instruct.request import ChatCompletionRequest

# tokenizer = MistralTokenizer.v3()

# def formatar_mensagens_para_texto(lista_mensagens: list[dict]) -> str:
#     """
#     Formata as mensagens em um formato mais legível para pessoas

#     Args:
#         lista_mensagens: list[dict] - lista de mensagens no formato padrão
    
#     Returns:
#         str: mensagens formatadas de forma amigável

#     """
#     if not lista_mensagens:
#         return ""

#     texto_formatado = []

#     for mensagem in lista_mensagens:
#         role = mensagem.get('role', '').strip()
#         content = mensagem.get('content', '').strip()

#         if role == "user":
#             texto_formatado.append(f"USUARIO: {content}")
#         elif role == "assistant":
#             texto_formatado.append(f"ASSISTENTE: {content}")
        
#     return "\n\n".join(texto_formatado)

# def contar_tokens_mensagens(lista_mensagens: list[dict]) -> int:
#     """
#     Conta o número de tokens de uma sequência de mensagens no formato esperado pela LLM.

#     Espera receber:
#     - `lista_mensagens`: list[dict] - uma lista de dicionários representando as mensagens
    
#     Formato esperado da lista:
#     ```json
#     [
#         {"role": "user", "content": <conteudo>},
#         {"role": "assistant", "content": <conteudo>},
#         ...
#     ]
#     ```
#     """
#     mensagens_formatadas = []

#     for m in lista_mensagens:
#         if m["role"] == "user":
#             mensagens_formatadas.append(UserMessage(content=m["content"]))
#         elif m["role"] == "assistant":
#             mensagens_formatadas.append(AssistantMessage(content=m["content"]))
#         else:
#             continue

#     request = ChatCompletionRequest(
#         messages=mensagens_formatadas,
#         model="mistral"
#     )

#     resultado = tokenizer.encode_chat_completion(request)
#     return len(resultado.tokens)

# def formatar_mensagem_salva(mensagem: dict) -> str:
#     """
#     Formata uma única mensagem salva do banco de dados.
    
#     Args:
#         mensagem: dict - Mensagem no formato do banco de dados
#             Exemplo: {'id': '...', 'chat_id': '...', 'sender_id': '...', 'conteudo': '...', 'data_envio': '...'}
    
#     Returns:
#         str: Mensagem formatada de forma limpa
#     """
#     if not mensagem or not isinstance(mensagem, dict):
#         return ""
    
#     sender_id = mensagem.get('sender_id', '')
#     conteudo = mensagem.get('conteudo', '').strip()
    
#     # Verifica se é do aluno ou da LLM (você pode ajustar essa lógica)
#     if sender_id == 'd34df2c4-ea93-4900-b92a-75f192abc72a':  # ID do aluno
#         return f"USUÁRIO: {conteudo}"
#     else:
#         return f"ASSISTENTE: {conteudo}"

# def formatar_mensagens_recentes(mensagens: list[dict]) -> str:
#     """
#     Formata uma lista de mensagens recentes do banco de dados.
    
#     Args:
#         mensagens: list[dict] - Lista de mensagens no formato do banco de dados
#             Exemplo: [{'id': '...', 'sender_id': '...', 'conteudo': '...'}, ...]
    
#     Returns:
#         str: Todas as mensagens formatadas de forma limpa
#     """
#     if not mensagens:
#         return ""
    
#     texto_formatado = []
    
#     for mensagem in mensagens:
#         if not isinstance(mensagem, dict):
#             continue
            
#         sender_id = mensagem.get('sender_id', '')
#         conteudo = mensagem.get('conteudo', '').strip()
        
#         if not conteudo:
#             continue
        
#         # Define o role baseado no sender_id
#         if sender_id == 'd34df2c4-ea93-4900-b92a-75f192abc72a':  # ID do aluno
#             role = "USUÁRIO"
#         else:
#             role = "ASSISTENTE"
        
#         texto_formatado.append(f"{role}: {conteudo}")
    
#     return "\n\n".join(texto_formatado)

# def formatar_mensagens_tokenizacao(mensagens: list[dict]) -> str:
#     """
#     Formata mensagens já preparadas para tokenização.
    
#     Args:
#         mensagens: list[dict] - Lista de mensagens no formato de tokenização
#             Exemplo: [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}]
    
#     Returns:
#         str: Mensagens formatadas de forma limpa
#     """
#     if not mensagens:
#         return ""
    
#     texto_formatado = []
    
#     for mensagem in mensagens:
#         if not isinstance(mensagem, dict):
#             continue
            
#         role = mensagem.get('role', '').lower()
#         content = mensagem.get('content', '').strip()
        
#         if not content:
#             continue
        
#         if role == 'user':
#             texto_formatado.append(f"USUÁRIO: {content}")
#         elif role == 'assistant':
#             texto_formatado.append(f"ASSISTENTE: {content}")
#         else:
#             # Para outros roles, usa o nome do role em maiúsculo
#             texto_formatado.append(f"{role.upper()}: {content}")
    
#     return "\n\n".join(texto_formatado)