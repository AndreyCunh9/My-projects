import os
import time
import pandas as pd
import pyautogui
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selecao_mes import selecionar_mes
from Credentiais import credenciais

# URL da página inicial
url = 'https://contribuinte.sefaz.al.gov.br/cobrancadfe/#/'


def get_unique_filename(base_directory, base_filename):
    counter = 0
    unique_filename = base_filename
    while os.path.exists(os.path.join(base_directory, unique_filename)):
        counter += 1
        name, ext = os.path.splitext(base_filename)
        unique_filename = f"{name}_{counter}{ext}"
    return unique_filename


def extrair_dados(username, password):
    # Iniciar o WebDriver

    driver = webdriver.Chrome()
    driver.maximize_window()
    data = []

    driver.get(url)
    time.sleep(5)

    try:

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="account-menu"]'))
        )
        login_button.click()

        entrar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]/span'))
        )
        entrar_button.click()

        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
        )

        username_field.send_keys(username)
        password_field.send_keys(password)

        entrar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/ngb-modal-window/div/div/jhi-login-modal/div[2]/div/div[2]/form/button'))
        )
        entrar_button.click()
        time.sleep(5)

        try:
            exit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/ngb-modal-window/div/div/jhi-mensagem-alerta/div[1]/button'))
            )
            exit_button.click()
        except TimeoutException:
            print("Elemento 'Sair' não encontrado. Continuando com o código.")

        cobranca_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="link-acesso-obrigacoes-acessorias"]'))
        )
        cobranca_button.click()

        selecionar_mes(driver)
        time.sleep(2)

        # Obter o número de cobranças
        texto_do_td = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="3-panel"]/div/jhi-datatable-dfe-expandedrows/div[2]/div/div['
                           '1]/fieldset/table/tbody/tr/td[1]'))
        ).text

        # Converte o texto em número
        numero = int(texto_do_td) * 2

        print('Tem', texto_do_td, 'cobranças nessa página')

        # Armazena os números encontrados para comparação
        numeros_encontrados = set()

        for i in range(1, numero + 1):
            print(f"Lendo o elemento tr numero: {i}")

            # XPath para o número do documento
            numero_xpath = f'/html/body/jhi-main/div[2]/div/jhi-calculo-nfe/div/div[1]/ngb-tabset/div/div/div/jhi-datatable-dfe-expandedrows/div[2]/table/tbody/tr[{i}]/td[2]'
            numero_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, numero_xpath))
            )
            numero_text = numero_element.text
            print('Numero:', numero_text)

            situacao_xpath = f'//*[@id="3-panel"]/div/jhi-datatable-dfe-expandedrows/div[2]/table/tbody/tr[{i}]/td[8]'
            situacao_element = driver.find_element(By.XPATH, situacao_xpath)
            situacao = situacao_element.text
            print('Situacao:', situacao)

            # Verificar se o número já foi encontrado
            if numero_text in numeros_encontrados:
                print(f"Numero duplicado encontrado: {numero_text}. Pulando para o próximo.")
                continue
            else:
                numeros_encontrados.add(numero_text)

            # Clique no número para abrir a janela modal
            expandir_DOC = (f'/html/body/jhi-main/div[2]/div/jhi-calculo-nfe/div/div[1]/ngb-tabset/div/div/div/jhi-datatable-dfe-expandedrows/div[2]/table/tbody/tr[{i}]/td[1]/i')
            numero_doc = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, expandir_DOC))
                                                         )
            numero_doc.click()
            print("Abrindo para ver os números das notas")

            # Clique no número para abrir a janela modal
            abrir_numero_doc = (f'/html/body/jhi-main/div[2]/div/jhi-calculo-nfe/div/div[1]/ngb-tabset/div/div/div/jhi-datatable-dfe-expandedrows/div[2]/table/tbody/tr[2]/td[2]')
            abrir_nmr_doc_modal = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, abrir_numero_doc))
                )
            abrir_nmr_doc_modal.click()
            print("Abrindo para ver os detalhes")

            # Aguarde a janela modal abrir
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/ngb-modal-window/div/div/jhi-detalhe-nota-item/div[2]'))
            )

            texto_h6 = driver.find_element(By.XPATH,
                                           '/html/body/ngb-modal-window/div/div/jhi-detalhe-nota-item/div[2]/div[1]/h6[2]').text
            print('A chave é', texto_h6)

            # Ler os valores na tabela dentro da janela modal
            row = 1
            while True:
                try:
                    # Tentar acessar a linha atual
                    xpath_tr = f'/html/body/ngb-modal-window/div/div/jhi-detalhe-nota-item/div[2]/div[2]/table/tbody/tr[{row}]'
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, xpath_tr))
                    )

                    col_data = [texto_h6]

                    # Percorrer as colunas dessa linha
                    for col in range(1, 12):
                        try:
                            xpath_td = f'{xpath_tr}/td[{col}]'
                            td_element = WebDriverWait(driver, 2).until(
                                EC.presence_of_element_located((By.XPATH, xpath_td))
                            )
                            td_text = td_element.text
                            col_data.append(td_text)
                            print(f'Valor da célula [{row}, {col}]: {td_text}')
                        except Exception as e:
                            print(f'Erro ao ler a célula [{row}, {col}]: {e}')

                    col_data.append(situacao)
                    data.append(col_data)

                    # Incrementar a linha para a próxima iteração
                    row += 1
                except Exception as e:
                    # Se a linha não for encontrada, sair do loop
                    print(f'Linha {row} não encontrada. Finalizando leitura do modal.')
                    break

            # Fechar a janela modal
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/ngb-modal-window/div/div/jhi-detalhe-nota-item/div[1]/button'))
            )
            close_button.click()
            time.sleep(1)

        #primeiros comandos para começar a emissao do relatorio e da guia de pagamento
        try:
            botao_st = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/jhi-main/div[2]/div/jhi-calculo-nfe/div/div[1]/ngb-tabset/ul/li['
                                            '3]/a/jhi-tab-set-title/div/div/span'))
            )
            botao_st.click()
            time.sleep(3)
            print('Clicando no st')

            botao_imrprimir_relat = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/jhi-main/div[2]/div/jhi-calculo-nfe/div/div[2]/div[2]/div/button'))
            )
            botao_imrprimir_relat.click()

            botao_imrprimir_relat_completo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/jhi-main/div[2]/div/jhi-calculo-nfe/div/div[2]/div[2]/div/div/div/div[1]'))
            )
            botao_imrprimir_relat_completo.click()

            time.sleep(5)

            janelas = driver.window_handles
            driver.switch_to.window(janelas[-1])

            pdf_url = driver.execute_script("return window.location.href;")
            print(pdf_url)

            # Verifique se o URL é um blob
            if pdf_url.startswith('blob:'):
                timestamp = int(time.time())
                base_filename = f'arquivo_{username}_{timestamp}_relat.pdf'
                unique_filename = get_unique_filename(r"C:\Users\andrey.cunha\Downloads\Guias", base_filename)
                js_code = f'''
                const blobUrl = "{pdf_url}";
                if (blobUrl.startsWith('blob:')) {{
                    fetch(blobUrl)
                        .then(response => response.blob())
                        .then(blob => {{
                            const url = window.URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.style.display = 'none';
                            a.href = url;
                            a.download = '{unique_filename}';
                            document.body.appendChild(a);
                            a.click();
                            window.URL.revokeObjectURL(url);
                        }})
                        .catch(error => console.error('Erro ao baixar o PDF:', error));
                }} else {{
                    console.error('O elemento embed não contém uma URL blob.');
                }}
                '''
                # Execute o código JavaScript no navegador
                driver.execute_script(js_code)
            else:
                print('O URL da aba não é um blob.')
            # Clique no botão de download

            #try:
            # Loop para tela inicial do tab
            #for _ in range(39):
            #pyautogui.press("tab")
            #print("Pressionou Tab")
            #time.sleep(2)

            #pyautogui.press("enter")
            #time.sleep(2)
            #print("Download iniciado.")
            #pyautogui.press("enter")
            #time.sleep(2)
            #print('Relatorio de cobrança de Doc fiscais')

            #except TimeoutException:
            #print("Elemento de download não encontrado.")

            # Obter todas as guias abertas
            janelas = driver.window_handles
            # Alternar para a última guia (a guia recém-aberta)
            driver.switch_to.window(janelas[0])
            time.sleep(2)
            #Clicar para emitir o documento de arrecadacao

            botao_doc_arrecad = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/jhi-main/div[2]/div/jhi-calculo-nfe/div/div[2]/div[3]/div'))
            )
            botao_doc_arrecad.click()
            time.sleep(1)

            botao_doc_arrecad_emit = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/jhi-main/div[2]/div/jhi-calculo-nfe/div/div[2]/div[3]/div/div/div/div[1]'))
            )
            botao_doc_arrecad_emit.click()
            time.sleep(1)

            botao_doc_arrecad_emit_conf = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/ngb-modal-window/div/div/jhi-confirmar-emissao-dar-consolidado/div[2]/div[3]/button[2]'))
            )
            botao_doc_arrecad_emit_conf.click()
            time.sleep(100)

            janelas = driver.window_handles
            driver.switch_to.window(janelas[-1])

            pdf_url = driver.execute_script("return window.location.href;")
            print(pdf_url)
            # Verifique se o URL é um blob
            if pdf_url.startswith('blob:'):
                timestamp = int(time.time())
                base_filename = f'arquivo_{username}_{timestamp}.pdf'
                unique_filename = get_unique_filename(r"C:\Users\andrey.cunha\Downloads\Guias", base_filename)
                js_code = f'''
                            const blobUrl = "{pdf_url}";
                            if (blobUrl.startsWith('blob:')) {{
                                fetch(blobUrl)
                                    .then(response => response.blob())
                                    .then(blob => {{
                                        const url = window.URL.createObjectURL(blob);
                                        const a = document.createElement('a');
                                        a.style.display = 'none';
                                        a.href = url;
                                        a.download = '{unique_filename}';
                                        document.body.appendChild(a);
                                        a.click();
                                        window.URL.revokeObjectURL(url);
                                    }})
                                    .catch(error => console.error('Erro ao baixar o PDF:', error));
                            }} else {{
                                console.error('O elemento embed não contém uma URL blob.');
                            }}
                            '''
                # Execute o código JavaScript no navegador
                driver.execute_script(js_code)
                time.sleep(5)
            else:
                print('O URL da aba não é um blob.')

                # Aperte no botão de download
                #try:
                #for _ in range(39):
                #pyautogui.press("tab")
                #print("Pressionou Tab")
                #time.sleep(2)

                #pyautogui.press("enter")
                #time.sleep(2)
                #print("Download iniciado.")
                #pyautogui.press("enter")
                #time.sleep(2)
                #print('Guias para pagamento baixada')
                #except TimeoutException:
                #print("Elemento de download não encontrado.")

                #voltar para guia inicial
                driver.switch_to.window(janelas[0])

        except TimeoutException:
            print('Nao conseguiu baixar nenhum documento')

    except TimeoutException:
        print("Tempo limite excedido ao tentar encontrar elementos na página.")

    return data
