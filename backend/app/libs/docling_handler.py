from docling.document_converter import DocumentConverter

def extrair_texto_markdown(caminho_arquivo):
    """
    Usa o Docling para extrair o texto do arquivo e retorná-lo em markdown.
    """
    converter = DocumentConverter()
    result = converter.convert(caminho_arquivo)
    return result.document.export_to_markdown()
