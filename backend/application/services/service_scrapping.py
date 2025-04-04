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
Devido aos erros de sintaxe gerados pelo scrapping, a funcao text_normalization foi criada para normalizar os textos
"""    
def text_normalization(text):
    return text.encode('utf-8', errors='ignore').decode('utf-8').strip() if text else ""

def extract_title(driver):
    titles = []
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        elements = driver.find_elements(By.TAG_NAME, tag)
        for element in elements:
            tittle_text = text_normalization(element.text)
            if tittle_text and not tittle_text.isspace():
                titles.append(tittle_text)
    return titles

def extract_paragraphs(driver):
    paragraphs = []
    elements = driver.find_elements(By.TAG_NAME, 'p')
    for element in elements:
        text = text_normalization(element.text)
        if text and not text.isspace():
            paragraphs.append(text)
    return paragraphs

def extract_links(driver):
    links = []
    elements = driver.find_elements(By.TAG_NAME, 'a')
    for element in elements:
        links.append(element.get_attribute('href'))
    return links

def extract_images(driver):
    images = []
    elements = driver.find_elements(By.TAG_NAME, 'img')
    for element in elements:
        images.append(element.get_attribute('src'))
    return images

def data_extraction(driver, url):
    try :
        print(f'Extraindo dados da URL: {url}')
        driver.get(url)
        time.sleep(2)
        
        # forçar a codificação para utf-8, Verifica e adiciona meta tag charset se não existir
        driver.execute_script("""
                    if (!document.querySelector('meta[charset]') && !document.querySelector('meta[http-equiv=\"Content-Type\"]')) {
                        var meta = document.createElement('meta');
                        meta.setAttribute('charset', 'UTF-8');
                        document.head.appendChild(meta);
                    }
                """)
        
        data = {
            'url': url,
            'page_title': driver.title,
            'titles': extract_title(driver),
            'paragraphs': extract_paragraphs(driver),
            'links': extract_links(driver),
            'images': extract_images(driver),
        }
        
        print(f'Dados extraídos com sucesso da URL: {url}')             
        return data
        
    except Exception as e:
        print(f'Erro ao extrair {url}: {str(e)}')
        return {
            'url': url,
            'status': 'error',
            'error_message': str(e)
        }
    
