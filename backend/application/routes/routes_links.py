from flask import Blueprint, request, jsonify
from application.services.service_scrapping import *
from urllib.parse import urlparse
import time


links_bp = Blueprint('links', __name__)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

@links_bp.route('/upload', methods=['POST'])
def scrap_links():
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
    driver = configure_browser()
    results = []
    
    try:
        for url in valid_urls:
            print(f'Processando URL: {url}')
            result = data_extraction(driver, url)
            results.append(result)
            time.sleep(2)
            
        return jsonify({
            "status": "success",
            'processed_url': len(valid_urls),
            "results": results   
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'processed_url': len(valid_urls),
            "error": str(e)
            }), 500
    finally:
        driver.quit()
        print('Driver fechado')