from application.mistral.core import pipeline

def main():
    pergunta = "O que é inteligência artificial?"
    resposta = pipeline.run(pergunta)
    print("Pergunta:", pergunta)
    print("Resposta:", resposta)

if __name__ == "__main__":
    main()
