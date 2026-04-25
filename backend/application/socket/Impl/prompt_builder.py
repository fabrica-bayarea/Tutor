def build_prompt(materia: str, contexto: list[str], historico: str, pergunta: str) -> str:

    contexto_txt = "\n".join(contexto) if contexto else ""

    return f"""
[SYSTEM]
Você é um tutor especialista em {materia}. 
Responda de forma estretruturada e educativa, formatada em markdown(com listas, negrito, título, etc) e em português a pergunta apresentada abaixo. 
Se a sessão de contexto deste prompt não estiver vazia, cite explicitamente trechos dela como fonte ao final da resposta. 
Caso a sessão de contexto esteja vazia, cite fontes internas do modelo ao final da resposta.

[CONTEXT]
{contexto_txt}

[HISTORICO]
{historico}

[USER]
{pergunta}
""".strip()
