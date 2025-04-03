from flask import Blueprint, request, jsonify
from application.services.service_scrapping import *
from urllib.parse import urlparse

links_bp = Blueprint('links', __name__)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

@links_bp.route('/upload', methods=['POST'])
def scrap_links():
    if not request.json or 'url' not in request.json:
        print('URL nao fornecida')
        return jsonify({"error": "URL não fornecida", "status": "error"}), 400
    
    print('REQUISICAO RECEBIDA') 
    
    url = request.json['url']
    driver = configure_browser()
    
    try:
        data = data_extraction(driver, url)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500
    finally:
        driver.quit()