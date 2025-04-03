from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def configure_browser():
    """
    Configura o navegador com opções de headless e idioma.
    """
    
    browser_options = Options()
    browser_options.add_argument('--headless') # Executar o navegador sem interface gráfica
    browser_options.add_argument('--disable-notifications') # Desabilitar notificação
    browser_options.add_argument('--lang=pt-BR') # Definir o idioma do navegador

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=browser_options)
    return driver



def data_extraction(driver, url):
    try :
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
        
        """
        titulo_pagina armazena o titulo da pagina
        url armazena a url da pagina
        titulos armazena os titulos encontrados na pagina
        paragrafos armazena os paragrafos encontrados na pagina
        """
        
        data = {
            'url': url,
            'page_title': driver.title,
            'titles': [],
            'paragraphs': [],
            'links': []
        }
    
        
        # funcao para normalizar o texto
        def text_normalization(text):
            return text.encode('utf-8', errors='ignore').decode('utf-8').strip()
        
        def extract_title():
            titles = []
            for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                elements = driver.find_elements(By.TAG_NAME, tag)
                for element in elements:
                    titles.append(text_normalization(element.text))
            return titles
        
        def extract_paragraphs():
            paragraphs = []
            elementos = driver.find_elements(By.TAG_NAME, 'p')
            for element in elementos:
                text = text_normalization(element.text)
                if text and not text.isspace():
                    paragraphs.append(text)
            return paragraphs
        
        def extract_links():
            links = []
            elements = driver.find_elements(By.TAG_NAME, 'a')
            for element in elements:
                links.append(element.get_attribute('href'))
            return links
        
        data['titles'] = extract_title()
        data['paragraphs'] = extract_paragraphs()
        data['links'] = extract_links()
                       
        return data
        
    except Exception as e:
        print(f'Ocorreu um erro: {str(e)}')
        return None
    
def main():
    
    # Atualmente o scrapping funciona apenas com uma url sendo passada como argumento, mas isso pode ser modificado futuramente
    url = 'https://www.selenium.dev/documentation/webdriver/drivers/'
    
    driver = configure_browser()
    
    try: 
        data = data_extraction(driver, url)
        if data:
            print('\nDadosExtraidos:')
            print(f'\nurl: {data["url"]}\n \nTitulo da pagina: {data["page_title"]}')
            
            print(f'\nTitulos encontrados: ')
            for i, title in enumerate(data['titles']):
                print(f'{i}. {title}')
                
            print(f'\nParagrafos encontrados: ')
            for i, paragraph in enumerate(data['paragraphs']):
                print(f'{i}. {paragraph}')
                
            print(f'\nLinks encontrados: ')
            for i, link in enumerate(data['links']):
                print(f'{i}. {link}')
        else: 
            print('Nao foi possivel extrair os dados')
            
    except Exception as e:
        print(f'Ocorreu um erro: {str(e)}')
        
    finally:
        driver.quit()
        
if __name__ == '__main__':
    main()
