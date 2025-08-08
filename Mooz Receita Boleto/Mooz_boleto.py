import pandas as pd
from lxml import html
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from aguardar_download import aguardar_download
import tkinter as tk
from tkinter import simpledialog
import os
import shutil
from datetime import datetime
import re
from urllib.parse import quote


def Extrair_boletos():
    tempo_inicio = time.time()

    # PARAMETROS DA CONSULTA
    lista_vd = ['20968', '20969', '20970', '20986', '20988', '20989', '20991', '20992', '20993', '20994', '20995',
                '20996',
                '20997', '20998', '20999', '21000', '21001', '21278', '21375', '21383', '21495', '22541']

    # OBTENDO AS DATAS DE INÍCIO E FIM USANDO TKINTER
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    data_inicio = simpledialog.askstring("Data de Início", "Digite a data de início (no formato DD/MM/AAAA):")
    data_fim = simpledialog.askstring("Data de Fim", "Digite a data de fim (no formato DD/MM/AAAA):")

    dia_hoje = datetime.today().strftime('%d')
    mes_hoje = datetime.today().strftime('%m')
    ano_hoje = datetime.today().strftime('%Y')

    # VARIÁVEIS
    ordem_download = 0

    pasta_downloads = 'C:/Users/andrey.cunha/Downloads/'
    # USUÁRIO E SENHA DO MOOZ BOLETOS
    usuario = "roberta.vanderlei@grupoginseng.com.br"
    senha = "W7946r**"

    # CODIFICANDO PARA URL
    data_inicio_URL = urllib.parse.quote(data_inicio, safe="")
    print(data_inicio_URL)
    data_fim_URL = urllib.parse.quote(data_fim, safe="")

    # URL DA CONSULTA MOOZ BOLETOS
    URL = f"https://www.moozboleto.com/portal/ufHome/index"

    # Configurar navegador Selenium
    driver = webdriver.Edge()
    driver.implicitly_wait(10)  # Configura um tempo limite de 10 segundos para todas as operações

    # AUTENTICAÇÃO DO USUÁRIO
    driver.get(URL)
    driver.maximize_window()
    driver.find_element(By.NAME, "username").send_keys(usuario)
    driver.find_element(By.NAME, "password").send_keys(senha)
    driver.find_element(By.XPATH, '//*[@id="entrar"]').click()

    for vd in lista_vd:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="header"]/nav/ul/li[4]/a/span')))
        # URL DO SERVIÇO
        URL_servico = f"https://www.moozboleto.com/portal/ufRecebimento/detalhamentoTitulos/?codigoFranquia={vd}&data={data_inicio_URL}&dataFim={data_fim_URL}"
        driver.get(URL_servico)

        # AGUARDAR A TABELA SER CARREGADA
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="extrairRelatorioDetalhamento"]')))

        # EXTRAIR RELATÓRIO
        driver.find_element(By.XPATH, '//*[@id="extrairRelatorioDetalhamento"]').click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="buttonList"]/div[1]/a')))
        driver.find_element(By.XPATH, '//*[@id="buttonList"]/div[1]/a').click()

        print('OK1')
        if ordem_download == 0:
            aguardar_download(f'{pasta_downloads}titulos_{dia_hoje}-{mes_hoje}-{ano_hoje}.csv')
        else:
            aguardar_download(f'{pasta_downloads}titulos_{dia_hoje}-{mes_hoje}-{ano_hoje} ({ordem_download}).csv')

        print(f'{lista_vd[ordem_download]} OK')
        ordem_download += 1

    driver.quit()

    # Caminhos das pastas
    download_folder = r'C:\Users\andrey.cunha\Downloads'
    destination_folder = r'C:\Users\andrey.cunha\Downloads\Receita'

    # Obter a data atual
    today = datetime.now()
    dia_hoje = datetime.today().strftime('%d')
    mes_hoje = datetime.today().strftime('%m')
    ano_hoje = datetime.today().strftime('%Y')

    # Padrão de nomeação dos arquivos
    pattern = rf'titulos_{dia_hoje}-{mes_hoje}-{ano_hoje}( \(\d+\))?\.csv'

    # Verificar se a pasta de destino existe, se não, criar
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Percorrer a pasta de downloads e mover os arquivos que correspondem ao padrão
    for filename in os.listdir(download_folder):
        if re.match(pattern, filename):
            source_path = os.path.join(download_folder, filename)
            destination_path = os.path.join(destination_folder, filename)
            shutil.move(source_path, destination_path)
            print(f'Movido: {filename} -> {destination_path}')

    diferenca_segundos = time.time() - tempo_inicio
    horas = int(diferenca_segundos // 3600)
    minutos = int((diferenca_segundos % 3600) // 60)
    segundos = int(diferenca_segundos % 60)

    diferenca_formatada = f"{horas:2d}:{minutos:2d}:{segundos:2d}"

    print(f'tempo total: {horas:2d}:{minutos:2d}:{segundos:2d}')
