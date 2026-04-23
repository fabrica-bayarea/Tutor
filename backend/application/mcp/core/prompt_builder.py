def build_prompt(materia: str, contexto: list[str], historico: str, pergunta: str) -> str:

    contexto_txt = "\n".join(contexto) if contexto else ""

    return f"""
[SYSTEM]
Você é um tutor especialista em {materia}. Responda de forma estretruturada e educativa, formatada em markdown e em português a pergunta apresentada abaixo. Se houver contexto, cite explicitamente trechos dele como fonte.

[CONTEXT]
{contexto_txt}

[HISTORICO]
{historico}

[USER]
{pergunta}
""".strip()
