from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('https://cnisnet.inss.gov.br/cnisinternet/faces/pages/index.xhtml')
res = True
mae = input ("Digite o nome da mãe: ")
nome = input ("Digite o nome: ")
data_nasc = input ("Digite a data de nascimento: ")
cpf = input ("Digite o CPF: ")
#https://cnisnet.inss.gov.br/cnisinternet/faces/pages/perfil.xhtml;jsessionid=mG6dkPJZL4T15p2vKdRtnK1X4CdMVzx2VgdNymvgptnHXbqPj1gD!-231581761

nit = ""
resultado_list = []
def executar_script(browser, nit):
    url = browser.current_url
    url_list = url.split(';')
    url2 = url_list[0]
    if url2 != 'https://cnisnet.inss.gov.br/cnisinternet/faces/pages/perfil.xhtml':
        print("Fechando navegador")
        browser.close()
        sleep(5)
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get('https://cnisnet.inss.gov.br/cnisinternet/faces/pages/index.xhtml')
    browser.find_element(By.ID, 'formEscolhaPerfis:perfilCidadao').click()
    sleep(2)
    browser.find_element(By.XPATH, '//*[@id="menu"]/ul/li/a').click()
    sleep(1)
    browser.find_element(By.ID, 'menu:inscricaoFiliadoCidadao').click()
    browser.find_element(By.ID, 'formse:nomeFiliado').send_keys(nome)
    browser.find_element(By.ID, 'formse:nomeMae').send_keys(mae)
    browser.find_element(By.ID, 'formse:dataNascimento_input').send_keys(data_nasc)
    browser.find_element(By.ID, 'formse:cpf').send_keys(cpf)
    #browser.find_element(By.CSS_SELECTOR, 'span.recaptcha-checkbox-border').click()
    input('Captcha')
    browser.find_element(By.ID, 'formse:continuar').click()
    resultado = browser.find_element(By.CLASS_NAME, 'ui-messages-error-detail').text
    print (resultado)
    resultado_list = resultado.split(' ')
    nit = resultado_list[22]
def verificador(nit):
    if nit.isdigit():
        print (f"{nit} é um número")
        nit_cartao = nit
        nome_nit = nome
        cpf_nit = cpf[0:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:11]
        data_nasc_nit = data_nasc[0:2] + '/' + data_nasc[2:4] + '/' + data_nasc[4:8]
        cartao_nit = {"nit" : f"PIS/PASEP/CNIS/NIS: {nit_cartao}",
    "name" : f"Nome: {nome_nit.upper()}",
    "cpf" : f"CPF: {cpf_nit}",
    "dataNasc" : f"Data de Nascimento: {data_nasc_nit}",
    }
        with open('nit.json', 'w') as f:
            json.dump(cartao_nit, f)
        os.chdir(os.path.dirname(os.path.abspath('index.html')))
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

        # Abra o navegador padrão
        webbrowser.open(f'http://localhost:{server_address[1]}/index.html')

        # Inicie o servidor
        print(f'Servindo na porta {server_address[1]}...')
        httpd.serve_forever()
        input()
        httpd.close_request()
        browser.quit()
        res=False
    else:
        pass

while res:
    try:
        executar_script(browser, nit)
        verificador(nit)
    except (IndexError, TypeError) as e:
        print (e)
        print (f"NIT não encontrado")
        mae = input ("Digite o nome da mãe: ")
        nome = input ("Digite o nome: ")
        data_nasc = input ("Digite a data de nascimento: ")
        cpf = input ("Digite o CPF: ")
        res=True
    else:
        print (f"NIT não encontrado")
        mae = input ("Digite o nome da mãe: ")
        nome = input ("Digite o nome: ")
        data_nasc = input ("Digite a data de nascimento: ")
        cpf = input ("Digite o CPF: ")
        res=True 
        
        

    
    
