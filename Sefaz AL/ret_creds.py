import pandas as pd
from Credentiais import credenciais
from extracao_dados import extrair_dados

def cred():
    todas_as_lojas_data = []
    credenciais_list = credenciais()

    for creds in credenciais_list:
        username = creds['username']
        password = creds['password']
        print(f"Extraindo dados para {username}")
        loja_data = extrair_dados(username, password)
        todas_as_lojas_data.extend(loja_data)

    columns = [
        'CHAVE DA NOTA', 'NUMERO DO ITEM', 'DESCRICAO', 'TIPO DO IMPOSTO', 'VLR ICMS', 'VLR FECOEP',
        'ALIQ ICMS', 'ALIQ FECOEP', 'MVA VALOR', 'REDUTOR', 'RED CREDITO', 'SEGMENTO', 'SITUACAO'
    ]
    df = pd.DataFrame(todas_as_lojas_data, columns=columns)
    df.to_excel(fr'C:\Users\andrey.cunha\Downloads\Calculo_Sefaz{username}.xlsx', index=False)
    print('Dados salvos na pasta')