import os
import time

def aguardar_download(nome_arquivo):
    i = 0
    while not os.path.exists(nome_arquivo):
        time.sleep(2)
        i += 1
        print(f'Esperando {i} segundos por {nome_arquivo}')

    base_nome, extensao = os.path.splitext(nome_arquivo)
    sequencia = 1
    while True:
        # Verifica se o arquivo com o número de sequência existe
        if os.path.isfile(nome_arquivo):
            if os.path.getsize(nome_arquivo) > 0:
                print(f'{nome_arquivo} baixado com sucesso.')
                return True
            else:
                print(f'{nome_arquivo} encontrado, mas tamanho zero. Continuando a esperar...')
                time.sleep(2)
        else:
            # Verifica se há outros arquivos com o mesmo nome base (sem número de sequência)
            encontrado = False
            for filename in os.listdir(os.path.dirname(nome_arquivo)):
                if filename.startswith(base_nome) and filename.endswith(extensao):
                    encontrado = True
                    break

            if encontrado:
                print(f'{nome_arquivo} encontrado. Continuando a esperar...')
                time.sleep(2)
            else:
                print(f'{nome_arquivo} não encontrado. Continuando a esperar...')
                time.sleep(2)

        # Incrementa o número de sequência para verificar o próximo arquivo numerado
        sequencia += 1
        nome_arquivo = f'{base_nome} ({sequencia}){extensao}'
