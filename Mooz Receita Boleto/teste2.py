import os
import time
import tkinter as tk
import webbrowser
from tkinter import simpledialog
from urllib.parse import quote
import shutil
from datetime import datetime
import pyautogui
from aguardar_download import aguardar_download

def Extrair_boletos():
    tempo_inicio = time.time()

    # PARAMETROS DA CONSULTA
    lista_vd = ['20968', '20969', '20970', '20986', '20988', '20989', '20991', '20992', '20993', '20994', '20995',
                '20996', '20997', '20998', '20999', '21000', '21001', '21278', '21375', '21383', '21495', '22541']

    # OBTENDO AS DATAS DE INÍCIO E FIM USANDO TKINTER
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    data_inicio = simpledialog.askstring("Data de Início", "Digite a data de início (no formato DD/MM/AAAA):")
    data_fim = simpledialog.askstring("Data de Fim", "Digite a data de fim (no formato DD/MM/AAAA):")

    # VARIÁVEIS
    dia_hoje = datetime.today().strftime('%d')
    mes_hoje = datetime.today().strftime('%m')
    ano_hoje = datetime.today().strftime('%Y')

    pasta_downloads = 'C:/Users/andrey.cunha/Downloads/'

    # Formatar as datas para URL
    data_inicio_URL = quote(data_inicio, safe='')
    data_fim_URL = quote(data_fim, safe='')

    # Loop para cada franquia
    for index, vd in enumerate(lista_vd):
        time.sleep(3)
        # URL do serviço de detalhamento de títulos para a franquia específica e datas
        URL_servico = f"https://www.moozboleto.com/portal/ufRecebimento/detalhamentoTitulos/?codigoFranquia={vd}&data={data_inicio_URL}&dataFim={data_fim_URL}"

        # Abrir o navegador padrão no URL específico
        webbrowser.open_new_tab(URL_servico)
        print(f'Consultando franquia {vd}...')

        # Esperar um tempo para a página carregar (ajustar conforme necessário)
        time.sleep(20)

        # Simular o clique no botão de extrair relatório (exemplo)
        pyautogui.click(1775, 469)
        time.sleep(3)
        pyautogui.click(890, 717)
        print('Simulando clique no botão de extrair relatório...')

        # Nome do arquivo a ser baixado
        if index == 0:
            nome_arquivo = f'titulos_{dia_hoje}-{mes_hoje}-{ano_hoje}.csv'
        else:
            nome_arquivo = f'titulos_{dia_hoje}-{mes_hoje}-{ano_hoje} ({index}).csv'

        caminho_arquivo = os.path.join(pasta_downloads, nome_arquivo)

        # Simular o download (usando a função aguardar_download)
        aguardar_download(caminho_arquivo)

        print(f'{vd} OK')

    diferenca_segundos = time.time() - tempo_inicio
    horas = int(diferenca_segundos // 3600)
    minutos = int((diferenca_segundos % 3600) // 60)
    segundos = int(diferenca_segundos % 60)

    print(f'Tempo total: {horas:2d}:{minutos:2d}:{segundos:2d}')

# Chamar a função para iniciar o processo
Extrair_boletos()
