import os
import shutil
from tkinter import Tk, Label, Button, Entry, messagebox
from tkinter import filedialog as fd
from bs4 import BeautifulSoup
from threading import Thread

def status_xml():
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

        # Criar pastas para cada tipo de XML
        tipos_xml = ['autorizado', 'cancelado', 'contingencia', 'inutilizado', 'cancelado pelo contribuinte']
        for tipo in tipos_xml:
            tipo_path = os.path.join(pasta_salvar, tipo)
            if not os.path.exists(tipo_path):
                os.makedirs(tipo_path)

        nf_status = {}  # Dicionário para armazenar o status de cada chNFe

        def atualizar_barra_progresso(valor):
            progresso.delete(0, 'end')
            progresso.insert(0, f"{valor}/{total_arquivos}")

        def extrair():
            for idx, arquivo_xml in enumerate(arquivos_xml, start=1):
                try:
                    with open(arquivo_xml, 'r') as arquivo:
                        xml = arquivo.read()

                    soup = BeautifulSoup(xml, 'xml')

                    # Extrair chNFe
                    chNFe = soup.find('chNFe').text if soup.find('chNFe') else None

                    # Verificar o código de status (cStat) para determinar o tipo de XML
                    tag_cStat = soup.find('cStat')
                    tag_xJust = soup.find('xJust')
                    tag_xServ =soup.find('xServ')

                    tipo_pasta = 'outros'
                    if tag_cStat and chNFe:
                        cStat = tag_cStat.text
                        if cStat == '100':
                            if chNFe in nf_status and nf_status[chNFe] == 'cancelado':
                                tipo_pasta = 'cancelado'
                            else:
                                tipo_pasta = 'autorizado'
                        elif cStat == '101':
                            tipo_pasta = 'cancelado'
                        elif cStat == '102':
                            tipo_pasta = 'inutilizado'
                        elif tag_xServ and "INUTILIZAR" in tag_xServ.text:
                            tipo_pasta = 'inutilizado'
                        elif cStat == '108':
                            if chNFe in nf_status and nf_status[chNFe] == 'autorizado':
                                tipo_pasta = 'autorizado'
                            else:
                                tipo_pasta = 'contingencia'
                        elif cStat == '135':
                            tipo_pasta = 'cancelado pelo contribuinte'

                        nf_status[chNFe] = tipo_pasta

                    # Verificar se a nota foi emitida em contingência pelo xJust
                    elif tag_xJust and "EMITIDA EM CONTINGENCIA" in tag_xJust.text:
                        tipo_pasta = 'contingencia'
                        if chNFe:
                            nf_status[chNFe] = tipo_pasta

                    caminho_destino = os.path.join(pasta_salvar, tipo_pasta, os.path.basename(arquivo_xml))

                    # Mover o arquivo para a pasta correta
                    shutil.move(arquivo_xml, caminho_destino)

                except Exception as e:
                    print(f"Erro ao processar o arquivo {arquivo_xml}: {e}")

                atualizar_barra_progresso(idx)
                progresso.update()  # Atualiza a barra de progresso

            mostrar_mensagem()

        t = Thread(target=extrair)
        t.start()

    def mostrar_mensagem():
        messagebox.showinfo("Concluído", "Extração de dados concluída!")

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

status_xml()
