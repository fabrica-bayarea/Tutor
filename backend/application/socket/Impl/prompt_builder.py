def build_prompt(materia: str, contexto: list[str], historico: str, pergunta: str) -> str:

    contexto_txt = "\n".join(contexto) if contexto else ""

    return f"""
[SYSTEM]
Você é um tutor especialista em {materia}. 
Responda de forma estretruturada e educativa, formatada em markdown(com listas, negrito, título, etc) e em português a pergunta apresentada abaixo. 
Use a sessão de contexto neste prompt como base da sua resposta e cite explicitamente trechos dela como fonte ao final da resposta. 

[CONTEXT]
{contexto_txt}

[HISTORICO]
{historico}

[USER]
{pergunta}
""".strip()
