from flask import Blueprint, request, jsonify, g
from urllib.parse import urlparse
import time
import uuid
from application.auth.auth_decorators import token_obrigatorio, apenas_professores
from application.services.service_arquivo import processar_link
from application.libs.scraping_handler import configure_browser
from application.utils.validacoes import validar_professor_turma_materia

links_bp = Blueprint('links', __name__)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

@links_bp.route('/upload', methods=['POST', 'OPTIONS'])
@token_obrigatorio
@apenas_professores
def scrap_links():
    
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'preflight'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    # Verifica se os dados necessários estão presentes
    urls = request.json.get('urls')
    vinculos = request.json.get('vinculos')
    
    if not urls:
        return jsonify({"error": "Parâmetro 'urls' é obrigatório"}), 400
    
    valid_urls = [url for url in urls if is_valid_url(url)]
    if not valid_urls:
        return jsonify({"error": "URL inválida"}), 400
    
    if not vinculos:
        return jsonify({"error": "Parâmetro 'vinculos' é obrigatório"}), 400
    
    # Valida os vínculos
    vinculos_processados: list[dict[str, uuid.UUID]] = []
    for vinculo in vinculos:
        try:
            turma_id = uuid.UUID(vinculo.get('turma_id'))
            materia_id = uuid.UUID(vinculo.get('materia_id'))
        except (ValueError, TypeError):
            return jsonify({"error": "IDs de turma e matéria devem ser UUIDs válidos"}), 400

        if not turma_id or not materia_id:
            return jsonify({"error": "Cada vínculo deve conter 'turma_id' e 'materia_id'"}), 400
        
        # Valida a existência do vínculo entre o professor, a turma e a matéria
        vinculo_existe = validar_professor_turma_materia(g.usuario_id, turma_id, materia_id)
        if not vinculo_existe:
            print(f"Vínculo entre professor '{g.usuario_id}', turma '{turma_id}' e matéria '{materia_id}' não encontrado")
            return jsonify({"error": f"Vínculo não encontrado para turma '{turma_id}' e matéria '{materia_id}'"}), 404
        
        # Adiciona o vínculo processado
        vinculos_processados.append({"turma_id": turma_id, "materia_id": materia_id})
    
    print(f'\nProcessando {len(valid_urls)} URLs')
    results = []

    try:
        print('Configurando driver')
        driver = configure_browser()
        print('Driver configurado')
        for url in valid_urls:
            print(f'Processando URL: {url}')
            result = processar_link(url, driver, g.usuario_id, vinculos_processados)
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
