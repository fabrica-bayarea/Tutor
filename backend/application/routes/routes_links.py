from flask import Blueprint, request, jsonify
from application.services.service_arquivo import *
from urllib.parse import urlparse
import time
import json
from application.services.service_arquivo import *
from application.services.service_professor import *
from application.services.service_turma import *
from application.services.service_materia import *

links_bp = Blueprint('links', __name__)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

@links_bp.route('/upload', methods=['POST', 'OPTIONS'])
def scrap_links():
    
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'preflight'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    if not request.json:
        return jsonify({"error": "URL não fornecida", "status": "error"}), 400
    
    urls = []
    if 'url' in request.json:
        urls = [request.json['url']] if isinstance(request.json['url'], str) else request.json['url']
    elif 'urls' in request.json:
        if isinstance(request.json['urls'], list):
            urls = request.json['urls']
        else:
            return jsonify({"error": "'urls' deve ser uma lista", "status": "error"}), 400
    else:
        return jsonify({"error": "Use 'url' ou 'urls'", "status": "error"}), 400
    
    valid_urls = [url for url in urls if is_valid_url(url)]
    if not valid_urls:
        return jsonify({"error": "URL inválida", "status": "error"}), 400
    
    print(f'\nProcessando {len(valid_urls)} URLs')
    results = []
    
    matricula_professor = request.json.get('matricula_professor')
    vinculos = request.json.get('vinculos') # Mesmo recebendo numa estrutura JSON, ele virá como string


    if not matricula_professor or not vinculos:
        return jsonify({"error": "Parâmetros 'matricula_professor' e 'vinculos' são obrigatórios"}), 400
    
    # Valida o professor
    professor_id = buscar_id_professor_por_matricula(matricula_professor)
    if not professor_id:
        print(f"Professor com matrícula '{matricula_professor}' não encontrado")
        return jsonify({"error": f"Professor com matrícula '{matricula_professor}' não encontrado"}), 404
    
    # Valida os vínculos
    vinculos_processados: list[dict[str, uuid.UUID]] = []
    for vinculo in vinculos:
        codigo_turma = vinculo.get('codigo_turma')
        codigo_materia = vinculo.get('codigo_materia')

        if not codigo_turma or not codigo_materia:
            return jsonify({"error": "Cada vínculo deve conter 'codigo_turma' e 'codigo_materia'"}), 400
        
        # Busca o UUID da turma
        turma_id = buscar_id_turma_por_codigo(codigo_turma)
        if not turma_id:
            print(f"Código de turma '{codigo_turma}' não encontrado")
            return jsonify({"error": f"Código de turma '{codigo_turma}' não encontrado"}), 404
        
        # Busca o UUID da matéria
        materia_id = buscar_id_materia_por_codigo(codigo_materia)
        if not materia_id:
            print(f"Código de matéria '{codigo_materia}' não encontrado")
            return jsonify({"error": f"Código de matéria '{codigo_materia}' não encontrado"}), 404
        
        # Adiciona o vínculo processado
        vinculos_processados.append({"turma_id": turma_id, "materia_id": materia_id})
    
    try:
        print('Configurando driver')
        driver = configure_browser()
        print('Driver configurado')
        for url in valid_urls:
            print(f'Processando URL: {url}')
            result = processar_link(url, driver, professor_id, vinculos_processados)
            results.append(result)
            print(f'URL processada com sucesso: {result}')
            time.sleep(2)
        driver.quit()
        return jsonify({
            "status": "success",
            'processed_url': len(valid_urls),
            "results": results
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'processed_url': len(valid_urls),
            "error": str(e)
            }), 500
    finally:
        driver.quit()
        print('Driver fechado')
