import os
import tempfile
import whisper

def extrair_audio(input_video: str, caminho_audio: str):
    """
    Usa FFmpeg para extrair e normalizar o áudio de um vídeo.

    Espera receber:
    - `input_video`: str - o caminho do arquivo de vídeo desejado
    - `caminho_audio`: str - o caminho onde será salvo o arquivo de áudio temporário

    Cria um arquivo de áudio temporário e retorna seu caminho.
    """
    print(f'\nIniciando extração de áudio do vídeo: {input_video}')
    ffmpeg_command = f"ffmpeg -i \"{input_video}\" -vn -acodec pcm_s16le -ar 16000 -ac 1 \"{caminho_audio}\" -y"
    os.system(ffmpeg_command)
    print(f'Áudio extraído em: {caminho_audio}')

def transcrever_audio(audio_file: str) -> str:
    """
    Usa Whisper para transcrever o áudio extraído.

    Espera receber:
    - `audio_file`: str - o caminho para o arquivo de áudio temporário
    
    Retorna a transcrição como texto.
    """
    print(f'Transcrevendo áudio com Whisper...')
    model = whisper.load_model("medium") # Ajustar conforme performance desejada
    result = model.transcribe(audio_file)
    return result["text"]

def processar_video(caminho_arquivo: str) -> str:
    """
    Processa um vídeo.

    Espera receber:
    - `caminho_arquivo`: str - o caminho do arquivo de vídeo
    
    1. Extrai o áudio do arquivo
    2. Transcreve o áudio com Whisper
    
    Retorna a transcrição como texto.
    """
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo de vídeo '{caminho_arquivo}' não foi encontrado.")
        return ""
    
    # Cria um arquivo temporário para o áudio extraído
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        caminho_audio = temp_audio.name
    
    try:
        # 1. Extrai o áudio do arquivo
        print(f'\n(1/2). Extraindo o áudio do arquivo')
        extrair_audio(caminho_arquivo, caminho_audio)
        print(f'ÁUDIO EXTRAÍDO COM SUCESSO!')

        if not os.path.exists(caminho_audio):
            print(f"Erro: O arquivo de áudio '{caminho_audio}' não foi gerado.")
            return ""

        # 2. Transcreve o áudio com Whisper
        print(f'\n(2/2). Transcrevendo o áudio com Whisper')
        transcricao = transcrever_audio(caminho_audio)
        print(f'TRANSCRIÇÃO CONCLUÍDA COM SUCESSO!')

        return transcricao
    
    finally:
        # Exclui o arquivo de áudio temporário
        if os.path.exists(caminho_audio):
            os.remove(caminho_audio)
