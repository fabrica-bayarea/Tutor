from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def configure_browser():
    """
    Configura o navegador com opções de headless e idioma.
    """    
    browser_options = Options()
    browser_options.add_argument('--headless')
    browser_options.add_argument('--disable-notifications')
    browser_options.add_argument('--lang=pt-BR')

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=browser_options)
     
     
     
"""
Devido aos erros de sintaxe gerados pelo scraping, a funcao text_normalization foi criada para normalizar os textos
"""    
def text_normalization(text):
    return text.encode('utf-8', errors='ignore').decode('utf-8').strip() if text else ""

def extract_body(driver): 
    body = driver.find_element(By.TAG_NAME, 'body')
    return text_normalization(body.text)


def data_extraction(driver, url):
    try :
        print(f'Extraindo dados da URL: {url}')
        driver.get(url)
        time.sleep(30)
        
        """
        forçar a codificação para utf-8, Verifica e adiciona meta tag charset se não existir
        """
        driver.execute_script("""
                    if (!document.querySelector('meta[charset]') && !document.querySelector('meta[http-equiv=\"Content-Type\"]')) {
                        var meta = document.createElement('meta');
                        meta.setAttribute('charset', 'UTF-8');
                        document.head.appendChild(meta);
                    }
                """)
        
        extracted_data = {
            'url': url,
            'page_title': str(driver.title),
            'content': extract_body(driver)
        }
        
        print(f'Dados extraídos com sucesso da URL: {url}')             
        return extracted_data
        
    except Exception as e:
        print(f'Erro ao extrair {url}: {str(e)}')
        return {
            'url': url,
            'status': 'error',
            'error_message': f'Falha ao carregar a URL: {str(e)}'
        }
    
