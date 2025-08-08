import datetime
import os
import time
import pyautogui
import pandas as pd
import shutil


def extrair_practico():
    input_data_ini = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%d%m%Y")
    input_data_fim = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%d%m%Y")
    previous_day = datetime.datetime.now() - datetime.timedelta(1)

    ignored_numbers_on_sunday = {85, 90, 91, 92, 93, 94, 95, 96, 102, 112, 113}

    input_numbers = [1, 3, 4, 22, 23, 24, 26, 28, 29, 30, 31, 32, 33, 36, 37, 39, 44, 48, 49, 52, 55, 56, 66, 82, 83,
                     84,
                     85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 104, 105, 106, 108, 109,
                     110, 111, 112, 113]

    if previous_day.weekday() == 6:
        input_numbers = [num for num in input_numbers if num not in ignored_numbers_on_sunday]

    time.sleep(5)

    app_path = (r"C:\Users\Ari Nascimento\AppData\Local\Apps\2.0\P3MZYEN1.WPT\BZE42JY9.JM5\live..tion_53587bf98d9a9d54_0006.0051_093c1b1618c305a8\PracticoLive.exe")

    try:
        os.startfile(app_path)
        print(f"Aplicativo {app_path} aberto com sucesso.")
    except Exception as e:
        print(f"Erro ao abrir o aplicativo: {e}")
    time.sleep(10)

    pyautogui.press("enter")
    time.sleep(5)
    pyautogui.press("enter")
    time.sleep(35)
    pyautogui.press("enter")
    time.sleep(5)
    print("Entrando no Practico")

    pyautogui.click(700, 242)
    time.sleep(5)
    pyautogui.press("alt")
    time.sleep(1)
    pyautogui.press("f")
    time.sleep(1)
    pyautogui.press("n")
    time.sleep(1)
    pyautogui.press("o")
    time.sleep(1)
    pyautogui.press("p")
    time.sleep(1)
    pyautogui.press("c")
    time.sleep(3)
    print("vai começar a extrair os relatórios")

    for i in range(6):
        pyautogui.press("tab")
    pyautogui.write(input_data_ini, interval=0.5)
    time.sleep(1)
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.write(input_data_fim, interval=0.5)

    selected_checkboxes = input_numbers

    def rename_downloaded_file(old_name, new_name):
        download_folder = r"C:\Users\Ari Nascimento\Desktop"
        old_file_path = os.path.join(download_folder, old_name)
        new_file_path = os.path.join(download_folder, new_name)

        if os.path.exists(old_file_path):
            os.rename(old_file_path, new_file_path)
            print(f'Arquivo renomeado de {old_name} para {new_name}')
        else:
            print(f'Erro: O arquivo {old_name} não foi encontrado.')

    def aguardar_download(nome_arquivo, timeout=30):
        download_folder = r"C:\Users\Ari Nascimento\Desktop"
        file_path = os.path.join(download_folder, nome_arquivo)

        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                print(f'{file_path} baixado com sucesso.')
                return True
            time.sleep(2)
        print(f'O arquivo {nome_arquivo} não foi encontrado no tempo esperado.')

        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.press("F12")

        return False

    def mark_checkbox(file_name, checkbox_number):
        time.sleep(3)
        for _ in range(3):
            time.sleep(1)
            pyautogui.press("tab")
        if checkbox_number >= 1:
            for _ in range(checkbox_number - 1):
                pyautogui.press("down")
        time.sleep(1)
        pyautogui.press("space")
        time.sleep(1)
        pyautogui.press("F10")
        time.sleep(1)
        pyautogui.press("F8")
        time.sleep(1)
        time.sleep(20)

        pyautogui.click(197, 200)
        pyautogui.press("down")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(5)

        if aguardar_download("VisualizarReceitas.xls"):
            rename_downloaded_file("VisualizarReceitas.xls", file_name)

        time.sleep(5)
        pyautogui.press("F12")
        time.sleep(1)
        pyautogui.press("alt")
        time.sleep(1)
        pyautogui.press("f")
        time.sleep(1)
        pyautogui.press("n")
        time.sleep(1)
        pyautogui.press("o")
        time.sleep(1)
        pyautogui.press("p")
        time.sleep(1)
        pyautogui.press("c")
        time.sleep(3)

        for i in range(6):
            pyautogui.press("tab")
        time.sleep(1)
        pyautogui.write(input_data_ini, interval=0.5)
        time.sleep(1)
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.write(input_data_fim, interval=0.5)

    def go_to_initial_position():
        time.sleep(1)
        pyautogui.click(74, 439)

    go_to_initial_position()

    downloaded_files = []

    for checkbox_number in selected_checkboxes:
        file_name = f"Loja_{checkbox_number}.xls"
        downloaded_files.append(os.path.join(r"C:\Users\Ari Nascimento\Desktop", file_name))
        mark_checkbox(file_name, checkbox_number)
        go_to_initial_position()

    def group_files(files_list, output_file):
        combined_df = pd.DataFrame()
        for file in files_list:
            if os.path.exists(file):
                try:
                    df = pd.read_excel(file)
                    df = df.dropna(subset=['Tipo Operação'])
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                except Exception as e:
                    print(f"Erro ao ler o arquivo {file}: {e}")
            else:
                print(f"Arquivo {file} não encontrado.")

        combined_df.to_excel(output_file, index=False)
        print(f"Arquivos agrupados no arquivo {output_file}")

        for file in files_list:
            try:
                os.remove(file)
                print(f"Arquivo {file} deletado com sucesso.")
            except Exception as e:
                print(f"Erro ao deletar o arquivo {file}: {e}")

        try:
            destination_path = r"T:\CONTAS A RECEBER\EEXTRATO\arquivo_agrupado.xlsx"
            shutil.move(output_file, destination_path)
            print(f"Arquivo movido para {destination_path} com sucesso.")
        except Exception as e:
            print(f"Erro ao mover o arquivo para {destination_path}: {e}")

    output_file = fr"C:\Users\Ari Nascimento\Desktop\arquivo_agrupado.xlsx"
    group_files(downloaded_files, output_file)
