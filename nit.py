from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import tkinter as tk
from tkinter import messagebox
    # Adicione aqui o código para buscar os dados usando as variáveis acima
def fechar():
    janela.destroy()
    

def buscar():
    nome1 = nome.get()
    mae1 = mae.get()
    cpf1 = cpf.get()
    data_nasc1 = data_nasc.get()
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get('https://cnisnet.inss.gov.br/cnisinternet/faces/pages/index.xhtml')
    nit = ""
    resultado_list = []
    browser.find_element(By.ID, 'formEscolhaPerfis:perfilCidadao').click()
    sleep(2)
    browser.find_element(By.XPATH, '//*[@id="menu"]/ul/li/a').click()
    sleep(1)
    browser.find_element(By.ID, 'menu:inscricaoFiliadoCidadao').click()
    browser.find_element(By.ID, 'formse:nomeFiliado').send_keys(nome1)
    browser.find_element(By.ID, 'formse:nomeMae').send_keys(mae1)
    browser.find_element(By.ID, 'formse:dataNascimento_input').send_keys(data_nasc1)
    browser.find_element(By.ID, 'formse:cpf').send_keys(cpf1)
    #browser.find_element(By.CSS_SELECTOR, 'span.recaptcha-checkbox-border').click()
    tk.messagebox.showinfo(title="CAPTCHA", message="Clique para continuar")
    browser.find_element(By.ID, 'formse:continuar').click()
    resultado = browser.find_element(By.CLASS_NAME, 'ui-messages-error-detail').text
    print (resultado)
    resultado_list = resultado.split(' ')
    nit = resultado_list[22]
    if nit.isdigit():
        print (f"{nit} é um número")
        nit_cartao = nit
        nome_nit = nome
        cpf_nit = cpf.get()[0:3] + '.' + cpf.get()[3:6] + '.' + cpf.get()[6:9] + '-' + cpf.get()[9:11]
        data_nasc_nit = data_nasc.get()[0:2] + '/' + data_nasc.get()[2:4] + '/' + data_nasc.get()[4:8]
        cartao_nit = {"nit" : f"PIS/PASEP/CNIS/NIS: {nit_cartao}",
    "name" : f"Nome: {nome_nit.get().upper()}",
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
        janela.messagebox.showinfo("Impressao", "Clique em OK apos imprimir o cartão")
        httpd.close_request()
        browser.quit()
    else:
        janela.messagebox.showinfo("Erro", "Erro ao buscar o NIT")

    
janela = tk.Tk()
janela.title("Busca de Dados")

nome = tk.StringVar(janela)
mae = tk.StringVar(janela)
cpf = tk.StringVar(janela)
data_nasc = tk.StringVar(janela)

tk.Label(janela, text="Nome:").grid(row=0, column=0, sticky="w")
tk.Entry(janela, textvariable=nome).grid(row=0, column=1)

tk.Label(janela, text="Nome da mãe:").grid(row=1, column=0, sticky="w")
tk.Entry(janela, textvariable=mae).grid(row=1, column=1)

tk.Label(janela, text="CPF:").grid(row=2, column=0, sticky="w")
tk.Entry(janela, textvariable=cpf).grid(row=2, column=1)

tk.Label(janela, text="Data de nascimento:").grid(row=3, column=0, sticky="w")
tk.Entry(janela, textvariable=data_nasc).grid(row=3, column=1)

tk.Button(janela, text="Buscar", command=buscar).grid(row=4, column=0, pady=10)
tk.Button(janela, text="Fechar", command=fechar).grid(row=4, column=1, pady=10)

janela.mainloop()


