import os
from bs4 import BeautifulSoup
import pyodbc
from Filial import mapeamento_cnpj_filial
from tkinter import filedialog as fd
from tkinter import Tk, Label, Button, Entry, messagebox
from datetime import datetime
from CFOP import mapeamento_cfop_nota
from openpyxl import Workbook
from threading import Thread
import itertools
from Status import status_xml
import shutil


status_xml()

# Configuração da conexão
conn_str = (
    'DRIVER={SQL Server};'
    'SERVER=10.77.77.10;'
    'DATABASE=p12_33;'
    'UID=fina;'
    'PWD=Ginseng@'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Carregar mapeamento de CNPJ/CPF para código de cliente
mapeamento_cgc_cliente = {}


# Função para gerar a sequência alfanumérica
def alfanumerico_sequencia():
    for size in range(1, 3):  # Adjust the range based on desired sequence length
        for s in itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', repeat=size):
            yield ''.join(s)


# Inicialize a sequência e o gerador alfanumérico
sequencia = 1
alfanumerico = alfanumerico_sequencia()


def carregar_mapeamento():
    query = """
    SELECT A1_CGC, A1_COD 
    FROM SA1010
    WHERE D_E_L_E_T_ =''
    """
    cursor.execute(query)
    for row in cursor.fetchall():
        cgc = row[0].strip()
        A1_COD = row[1].strip()
        mapeamento_cgc_cliente[cgc] = A1_COD


carregar_mapeamento()  # Chamar função para carregar o mapeamento


def buscar_xmls():
    pasta_xml = fd.askdirectory()
    entrada_caminho_xml.delete(0, 'end')
    entrada_caminho_xml.insert(0, pasta_xml)


def buscar_salvar():
    pasta_salvar = fd.askdirectory()
    entrada_caminho_salvar.delete(0, 'end')
    entrada_caminho_salvar.insert(0, pasta_salvar)


# Função para listar todos os arquivos XML em uma pasta
def listar_arquivos_xml(pasta):
    arquivos_xml = []
    for raiz, diretorios, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            if arquivo.endswith(".xml"):
                arquivos_xml.append(os.path.join(raiz, arquivo))
    return arquivos_xml


# Lista para armazenar CPFs e CNPJs extraídos
cnpjs_cpfs = set()

dict_mod = {'55': 'SPED', '65': 'NFCE'}
dict_cpf = {'27': 'CFAL0001', '28': 'CFSE0001', '29': 'CFBA0001'}


def extrair_dados():
    pasta_xml = entrada_caminho_xml.get()
    pasta_salvar = entrada_caminho_salvar.get()

    if not os.path.isdir(pasta_xml):
        print("Caminho da pasta XML inválido.")
        return

    if not os.path.isdir(pasta_salvar):
        print("Caminho da pasta para salvar inválido.")
        return

    arquivos_xml = listar_arquivos_xml(pasta_xml)
    total_arquivos = len(arquivos_xml)

    def atualizar_barra_progresso(valor):
        progresso.delete(0, 'end')
        progresso.insert(0, f"{valor}/{total_arquivos}")

    def extrair():
        arquivo_excel = Workbook()
        planilha = arquivo_excel.active

        chaves_numeros = {}

        # Extrair CPFs e CNPJs dos XMLs
        for idx, arquivo_xml in enumerate(arquivos_xml, start=1):
            try:
                with open(arquivo_xml, 'r') as arquivo:
                    xml = arquivo.read()

                soup = BeautifulSoup(xml, 'xml')

                # Dados principais
                CNPJ = soup.find('CNPJ').text if soup.find('CNPJ') else "CNPJ não encontrado"
                CNPJ = mapeamento_cnpj_filial.get(CNPJ, "Filial não encontrada para este CNPJ")

                nNF = soup.find('nNF').text.zfill(9) if soup.find('nNF') else (
                    soup.find('nNFFin').text if soup.find('nNFFin') else (chaves_numeros.get(soup.find('chNFe').text,
                                                                                             "Tag nNF, nNFFin e chNFe "
                                                                                             "não encontradas no "
                                                                                             "XML.") if soup.find(
                        'chNFe') else "Tag nNF, nNFFin e chNFe não encontradas no XML."))
                serie = soup.find('serie').text if soup.find('serie') else "Serie nao identificada"

                dest_doc = None
                dest_doc_tag = soup.find('dest')
                if dest_doc_tag:
                    if dest_doc_tag.find('CNPJ'):
                        dest_doc = dest_doc_tag.find('CNPJ').text
                    elif dest_doc_tag.find('CPF'):
                        dest_doc = dest_doc_tag.find('CPF').text

                uf = soup.find('cUF').text if soup.find('cUF') else "UF nao localizada"

                if dest_doc:
                    dest_doc = mapeamento_cgc_cliente.get(dest_doc, None)
                    if not dest_doc:
                        dest_doc = dict_cpf.get(uf, "Nao encontrado")
                else:
                    dest_doc = dict_cpf.get(uf, "Nao encontrado")

                print(dest_doc)

                xloja = soup.find('xloja').text if soup.find('xloja') else "01"

                dhRecbto_raw = soup.find('dhRecbto').text if soup.find('dhRecbto') else (
                    soup.find('dhEvento').text if soup.find('dhEvento') else "Não tem informações de processamento")
                if dhRecbto_raw not in ["", "Não tem informações de processamento"]:
                    dhRecbto = datetime.fromisoformat(dhRecbto_raw).strftime('%d/%m/%Y')
                else:
                    dhRecbto = dhRecbto_raw

                mod = soup.find('mod').text if soup.find('mod') else "Modelo nao localizado"
                mod = dict_mod.get(mod, "Revisar")

                chNFe = soup.find('chNFe').text if soup.find('chNFe') else \
                    os.path.splitext(os.path.basename(arquivo_xml))[0][:44]

                xtipo = soup.find('xtipo').text if soup.find('xtipo') else "N"

                for item in soup.find_all('total'):
                    vDesc = (item.find('vDesc').text.replace('.', ',')) if soup.find('vDesc') else ""

                vFrete = soup.find('vFrete').text.replace('.', ',') if soup.find('vFrete') else ""

                vSeg = soup.find('vSeg').text.replace('.', ',') if soup.find('vSeg') else ""

                # Salvar chave e número da nota no dicionário
                if soup.find('chNFe'):
                    chaves_numeros[soup.find('chNFe').text] = nNF

                # Linha de dados principais
                planilha.append(
                    ["SF2", CNPJ, nNF, serie, dest_doc, xloja, dhRecbto, mod, chNFe, xtipo, vDesc, vFrete, vSeg, ";"])
                sequencia = 1

                # Linhas de dados detalhados
                for item in soup.find_all('det'):
                    cod = (item.find('cProd').text if item.find('cProd') else 'N/A')
                    quant = int(float(item.find('qCom').text.replace(',', '.'))) if item.find('qCom') else 'N/A'
                    valor_unitario = format(float(item.find('vUnCom').text.replace(',', '.')), '.2f').replace('.',
                                                                                                              ',') if item.find(
                        'vUnCom') else 'N/A'
                    valor_total = format(float(item.find('vProd').text.replace(',', '.')), '.2f').replace('.',
                                                                                                          ',') if item.find(
                        'vProd') else 'N/A'

                    armazem = item.find('varmazem').text if item.find('varmazem') else '02'
                    icms = '0,00'  # Valor padrão
                    imposto = item.find('imposto')
                    if imposto:
                        icms_tag = imposto.find('pICMS')
                        if icms_tag:
                            icms = icms_tag.text.replace(',', '.')
                            icms = f"{float(icms):.2f}".replace('.', ',')
                        else:
                            "N/A"

                    cfop = (item.find('CFOP').text if item.find('CFOP') else 'N/A')
                    cfop = mapeamento_cfop_nota.get(cfop, "Nao tem TES")

                    # Ajustar a sequência para alfanumérica após 99
                    if sequencia <= 99:
                        seq_str = str(sequencia).zfill(2)
                    else:
                        seq_str = next(alfanumerico)
                    planilha.append(["SD2", cod, quant, cfop, valor_unitario, valor_total, armazem,
                                     str(str.zfill(str(sequencia), 2)), icms])
                    sequencia += 1

                atualizar_barra_progresso(idx)
                progresso.update()  # Atualiza a barra de progresso

            except Exception as e:
                print(f"Erro ao processar o arquivo {arquivo_xml}: {e}")

        caminho_arquivo = os.path.join(pasta_salvar, "Importar notas.xlsx")
        arquivo_excel.save(caminho_arquivo)
        print(f"Arquivo Excel salvo em: {caminho_arquivo}")

        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()

        mostrar_mensagem()

    def mostrar_mensagem():
        messagebox.showinfo("Concluído", "Extração de dados concluída!")

    t = Thread(target=extrair)
    t.start()


# Interface gráfica
root = Tk()
root.title("Extrair Dados de XML para Excel")

label_caminho_xml = Label(root, text="Caminho da pasta com os XMLs:")
label_caminho_xml.grid(row=0, column=0)

entrada_caminho_xml = Entry(root, width=50)
entrada_caminho_xml.grid(row=0, column=1)

botao_buscar_xmls = Button(root, text="Buscar", command=buscar_xmls)
botao_buscar_xmls.grid(row=0, column=2)

label_caminho_salvar = Label(root, text="Caminho da pasta para salvar o arquivo Excel:")
label_caminho_salvar.grid(row=1, column=0)

entrada_caminho_salvar = Entry(root, width=50)
entrada_caminho_salvar.grid(row=1, column=1)

botao_buscar_salvar = Button(root, text="Buscar", command=buscar_salvar)
botao_buscar_salvar.grid(row=1, column=2)

progresso = Entry(root, width=50)
progresso.grid(row=2, column=1)

botao_extrair = Button(root, text="Extrair Dados", command=extrair_dados)
botao_extrair.grid(row=3, column=1)

root.mainloop()
