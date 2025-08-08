import pandas as pd
from Cnpj_lojas import mapeamento_cnpj_filial  # Importe sua função de mapeamento de CNPJ para filial
from Tipo_de_pag import mapeamento_pag_tipo

# Passo 1: Ler o arquivo CSV
caminho_excel_eextrato = r"C:\Users\andrey.cunha\Downloads\baixaArquivo.xlsx"
df = pd.read_excel(caminho_excel_eextrato)

caminho_excel_protheus = r"C:\Users\andrey.cunha\Downloads\SE1.xlsx"
df_protheus = pd.read_excel(caminho_excel_protheus)

# Selecionar múltiplas colunas
colunas_selecionadas = df[['Filiais', 'Dados Cliente', 'Tipo Produto', 'Parcela', 'Valor Pago (R$)', 'Data do Pagamento']]

# Renomear as colunas selecionadas
colunas_selecionadas = colunas_selecionadas.rename(columns={
    'Filiais': 'FILIAL',
    'Dados Cliente': 'TITULO',
    'Tipo Produto': 'TIPO',
    'Valor Pago (R$)': 'VALOR',
    'Parcela': 'PARCELA',
    'Data do Pagamento': 'DATA_BAIXA'
})

# Inserir 4 novas colunas
colunas_selecionadas['BANCO'] = 'B03'
colunas_selecionadas['AGENCIA'] = '4494'
colunas_selecionadas['CONTA'] = '4494'
colunas_selecionadas['PREFIXO'] = ''

# Mapear CNPJ para FILIAL usando sua função
colunas_selecionadas['FILIAL'] = colunas_selecionadas['FILIAL'].map(mapeamento_cnpj_filial)
# Aplicar a condição usando expressão regular para identificar 'À Vista' independentemente da codificação
colunas_selecionadas['TIPO'] = colunas_selecionadas['TIPO'].map(mapeamento_pag_tipo)

colunas_selecionadas['PARCELA'] = colunas_selecionadas['PARCELA'].astype(str).str.split('.').str[0].str.zfill(2)

# Preencher a coluna 'TITULO' com zeros à esquerda até que tenha 9 caracteres
colunas_selecionadas['TITULO'] = colunas_selecionadas['TITULO'].fillna(0).astype(int).astype(str).str.zfill(9)

# Apagar a última linha do DataFrame
colunas_selecionadas = colunas_selecionadas.iloc[:-1]

# Converter a coluna de data para o formato DD/MM/AAAA
colunas_selecionadas['DATA_BAIXA'] = pd.to_datetime(colunas_selecionadas['DATA_BAIXA']).dt.strftime('%d/%m/%Y')

# Definir a ordem desejada das colunas
ordem_colunas = [
    'FILIAL', 'PREFIXO', 'PARCELA', 'TIPO', 'TITULO', 'BANCO', 'AGENCIA'
    , 'CONTA', 'DATA_BAIXA', 'VALOR'
]

# Reordenar as colunas do DataFrame
colunas_selecionadas = colunas_selecionadas.reindex(columns=ordem_colunas)

# Especificar o caminho completo onde você deseja salvar o arquivo
caminho_saida = r"C:\Users\andrey.cunha\Downloads\baixaArquivo_modificado.xlsx"

# Exportar o DataFrame para um arquivo CSV
colunas_selecionadas.to_excel(caminho_saida, index=False)

print(f"Arquivo salvo em: {caminho_saida}")
print(colunas_selecionadas)
