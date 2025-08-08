from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from Credentiais import credenciais
from extracao_dados import extrair_dados
import openpyxl
def cred():
    todas_as_lojas_data = []
    credenciais_list = credenciais()

    for creds in credenciais_list:
        username = creds['username']
        password = creds['password']
        print(f"Extraindo dados para {username}")
        loja_data = extrair_dados(username, password)
        todas_as_lojas_data.extend(loja_data)

        # Pega a data atual e subtrai um mês
    mes_ano_atual = (datetime.now() - relativedelta(months=1)).strftime('%m%Y')

    columns = [
        'CHAVE DA NOTA', 'NUMERO DO ITEM', 'DESCRICAO', 'TIPO DO IMPOSTO', 'VLR ICMS', 'VLR FECOEP',
        'ALIQ ICMS', 'ALIQ FECOEP', 'MVA VALOR', 'REDUTOR', 'RED CREDITO', 'SEGMENTO', 'SITUACAO'
    ]
    df = pd.DataFrame(todas_as_lojas_data, columns=columns)
    df.to_excel(fr'C:\Users\andrey.cunha\Downloads\Calculo_Sefaz_ST_{mes_ano_atual}.xlsx', index=False)
    print('Dados salvos na pasta')