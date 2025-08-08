import os
from datetime import datetime
from threading import Thread
from tkinter import Tk, Label, Button, Entry, messagebox
from tkinter import filedialog as fd
from bs4 import BeautifulSoup
from openpyxl import Workbook
from Filial import mapeamento_cnpj_filial


def buscar_xmls():
    pasta_xml = fd.askdirectory()
    entrada_caminho_xml.delete(0, 'end')
    entrada_caminho_xml.insert(0, pasta_xml)


def buscar_salvar():
    pasta_salvar = fd.askdirectory()
    entrada_caminho_salvar.delete(0, 'end')
    entrada_caminho_salvar.insert(0, pasta_salvar)


def listar_arquivos_xml(pasta):
    arquivos_xml = []
    for raiz, diretorios, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            if arquivo.endswith(".xml"):
                arquivos_xml.append(os.path.join(raiz, arquivo))
    return arquivos_xml


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

        for idx, arquivo_xml in enumerate(arquivos_xml, start=1):
            try:
                with open(arquivo_xml, 'r') as arquivo:
                    xml = arquivo.read()

                soup = BeautifulSoup(xml, 'xml')

                # Dados principais
                nNF = soup.find('nNF').text.zfill(9) if soup.find('nNF') else (
                    soup.find('nNFFin').text if soup.find('nNFFin') else (chaves_numeros.get(soup.find('chNFe').text,
                                                                                             "Tag nNF, nNFFin e chNFe "
                                                                                             "não encontradas no "
                                                                                             "XML.") if soup.find(
                        'chNFe') else "Tag nNF, nNFFin e chNFe não encontradas no XML."))
                vNF = soup.find('vNF').text.replace('.', ',') if soup.find('vNF') else "Valor nao eonctrado"
                vBC = soup.find('vBC').text.replace('.', ',') if soup.find('vBC') else "Base icms nao encontrada"
                vICMS = soup.find('vICMS').text.replace('.', ',') if soup.find('vICMS') else "Sem valor de ICMS"
                vDesc = soup.find('vDesc').text.replace('.', ',') if soup.find('vDesc') else ""
                CNPJ = soup.find('CNPJ').text if soup.find('CNPJ') else "CNPJ não encontrado"
                # Encontra o valor correspondente no mapeamento de CNPJ para filial
                CNPJ = mapeamento_cnpj_filial.get(CNPJ, "Filial não encontrada para este CNPJ")
                chNFe = soup.find('chNFe').text if soup.find('chNFe') else \
                    os.path.splitext(os.path.basename(arquivo_xml))[0][:44]
                vFrete = soup.find('vFrete').text.replace('.', ',') if soup.find('vFrete') else ""
                vSeg = soup.find('vSeg').text.replace('.', ',') if soup.find('vSeg') else ""
                dhRecbto_raw = soup.find('dhRecbto').text if soup.find('dhRecbto') else (
                    soup.find('dhEvento').text if soup.find('dhEvento') else "Não tem informações de processamento")
                if dhRecbto_raw not in ["", "Não tem informações de processamento"]:
                    dhRecbto = datetime.fromisoformat(dhRecbto_raw).strftime('%d/%m/%Y')
                else:
                    dhRecbto = dhRecbto_raw

                # Salvar chave e número da nota no dicionário
                if soup.find('chNFe'):
                    chaves_numeros[soup.find('chNFe').text] = nNF

                # Linha de dados principais
                planilha.append(
                    [CNPJ, nNF, chNFe, dhRecbto, vNF, vBC, vICMS, vDesc, vFrete, vSeg])

                atualizar_barra_progresso(idx)
                progresso.update()  # Atualiza a barra de progresso
            except Exception as e:
                print(f"Erro ao processar o arquivo {arquivo_xml}: {e}")

        caminho_arquivo = os.path.join(pasta_salvar, "Nfce.xlsx")
        arquivo_excel.save(caminho_arquivo)
        print(f"Arquivo Excel salvo em: {caminho_arquivo}")

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
