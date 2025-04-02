import os
import whisper

def extrair_caminho_arquivo(caminho_arquivo):
    """
    Lê o arquivo e retorna seu conteúdo como uma string (assumindo que seja um caminho de arquivo de vídeo).
    """
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return f.read().strip()

def processar_video(input_video, output_audio):
    """
    Usa FFmpeg para extrair e normalizar o áudio de um vídeo.
    """
    ffmpeg_command = f"ffmpeg -i {input_video} -vn -acodec pcm_s16le -ar 16000 -ac 1 {output_audio}"
    os.system(ffmpeg_command)

def transcrever_audio(audio_file):
    """
    Usa Whisper para transcrever o áudio extraído.
    """
    model = whisper.load_model("medium")  # Pode ser "tiny", "base", "small", "medium" ou "large"
    result = model.transcribe(audio_file)
    return result["text"]

def salvar_transcricao(transcricao, output_file):
    """
    Salva a transcrição em um arquivo de texto.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(transcricao)

def main():
    caminho_txt = "caminho_do_arquivo.txt"  # Substitua pelo caminho do arquivo que contém o caminho do vídeo
    input_video = extrair_caminho_arquivo(caminho_txt)
    output_audio = "normalized_audio.wav"  
    output_text = "outputs/transcription.txt"
    
    if not os.path.exists(input_video):
        print(f"Erro: O arquivo de vídeo '{input_video}' não foi encontrado.")
        return
    
    print("Processando vídeo com FFmpeg...")
    processar_video(input_video, output_audio)
    
    if not os.path.exists(output_audio):
        print(f"Erro: O arquivo de áudio '{output_audio}' não foi gerado.")
        return
    
    print("Transcrevendo áudio com Whisper...")
    transcricao = transcrever_audio(output_audio)
    
    print("Salvando transcrição...")
    salvar_transcricao(transcricao, output_text)
    
    print(f"Transcrição salva em '{output_text}'")