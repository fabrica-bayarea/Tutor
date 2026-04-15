def build_prompt(materia: str, contexto: list[str], historico: str, pergunta: str) -> str:

    contexto_txt = "\n".join(contexto) if contexto else ""

    return f"""
[SYSTEM]
Você é um tutor especialista em {materia}.

[CONTEXT]
{contexto_txt}

[HISTORICO]
{historico}

[USER]
{pergunta}
""".strip()