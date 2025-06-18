from flask import Blueprint, request, jsonify
from application.mistral.core import pipeline

rag_bp = Blueprint("rag", __name__)

@rag_bp.route("/perguntar", methods=["POST"])
def perguntar():
    data = request.json
    pergunta = data.get("pergunta", "")

    if not pergunta:
        return jsonify({"erro": "Campo 'pergunta' obrigatório"}), 400

    resposta = pipeline.run(pergunta)
    return jsonify({"resposta": resposta})