import pandas as pd
from Cnpj_lojas import mapeamento_cnpj_filial  # Importe sua função de mapeamento de CNPJ para filial
from Tipo_de_pag import mapeamento_pag_tipo

# Passo 1: Ler os arquivos Excel
caminho_excel_eextrato = r"C:\Users\andrey.cunha\Downloads\baixaArquivo.xlsx"
caminho_csv_protheus = r"C:\Users\andrey.cunha\Downloads\Protheus.csv"

# Ler as planilhas
df = pd.read_excel(caminho_excel_eextrato)

# Tentar ignorar linhas mal formatadas
try:
    df_protheus = pd.read_csv(caminho_csv_protheus, encoding='latin1', delimiter=';', on_bad_lines='skip')
    print("Colunas do DataFrame df_protheus:", df_protheus.columns)
except Exception as e:
    print(f"Erro ao ler o arquivo CSV: {e}")

# Verificar se a coluna 'No. Titulo' existe
if 'No. Titulo' in df_protheus.columns:
    df_protheus['No. Titulo'] = df_protheus['No. Titulo'].astype(str)
else:
    print("A coluna 'No. Titulo' não existe no DataFrame df_protheus.")
    print("Colunas disponíveis:", df_protheus.columns)

# Selecionar múltiplas colunas e renomear
colunas_selecionadas = df[['Filiais', 'Dados Cliente', 'Tipo Produto', 'Parcela', 'Valor Pago (R$)', 'Data do Pagamento']]

colunas_selecionadas = colunas_selecionadas.rename(columns={
    'Filiais': 'FILIAL',
    'Dados Cliente': 'TITULO',
    'Tipo Produto': 'TIPO',
    'Valor Pago (R$)': 'VALOR',
    'Parcela': 'PARCELA',
    'Data do Pagamento': 'DATA_BAIXA'
})

# Inserir colunas adicionais
colunas_selecionadas['BANCO'] = 'B03'
colunas_selecionadas['AGENCIA'] = '4494'
colunas_selecionadas['CONTA'] = '4494'
colunas_selecionadas['PREFIXO'] = ''

# Mapear CNPJ para FILIAL usando sua função
colunas_selecionadas['FILIAL'] = colunas_selecionadas['FILIAL'].map(mapeamento_cnpj_filial)

# Aplicar a condição usando expressão regular para identificar 'À Vista' independentemente da codificação
colunas_selecionadas['TIPO'] = colunas_selecionadas['TIPO'].map(mapeamento_pag_tipo)

# Manipular a coluna PARCELA
colunas_selecionadas['PARCELA'] = colunas_selecionadas['PARCELA'].astype(str).str.split('.').str[0].str.zfill(2)

# Preencher a coluna TITULO com zeros à esquerda até que tenha 9 caracteres
colunas_selecionadas['TITULO'] = colunas_selecionadas['TITULO'].fillna(0).astype(int).astype(str).str.zfill(9)

# Remover a última linha do DataFrame
colunas_selecionadas = colunas_selecionadas.iloc[:-1]

# Converter a coluna E1_NUM para inteiro
if 'No. Titulo' in df_protheus.columns:
    df_protheus['No. Titulo'] = df_protheus['No. Titulo'].astype(str).str.zfill(9)

# Converter a coluna E1_FILIAL para tipo object
if 'Filial' in df_protheus.columns:
    df_protheus['Filial'] = df_protheus['Filial'].astype(str).str.zfill(6)

# Converter a coluna DATA_BAIXA para o formato DD/MM/AAAA
colunas_selecionadas['DATA_BAIXA'] = pd.to_datetime(colunas_selecionadas['DATA_BAIXA']).dt.strftime('%d/%m/%Y')

# Realizando o merge usando pandas e selecionando as colunas desejadas
if 'No. Titulo' in df_protheus.columns and 'Filial' in df_protheus.columns:
    Prefixo_protheus = colunas_selecionadas.merge(df_protheus[['No. Titulo', 'Prefixo', 'Filial']],
                                                  how='left',
                                                  left_on=['TITULO', 'FILIAL'],
                                                  right_on=['No. Titulo', 'Filial'])
    colunas_selecionadas['PREFIXO'] = Prefixo_protheus['Prefixo']

# Definir a ordem desejada das colunas
ordem_colunas = [
    'FILIAL', 'PREFIXO', 'PARCELA', 'TIPO', 'TITULO', 'BANCO', 'AGENCIA',
    'CONTA', 'DATA_BAIXA', 'VALOR'
]

# Reordenar as colunas do DataFrame
colunas_selecionadas = colunas_selecionadas.reindex(columns=ordem_colunas)

# Especificar o caminho completo onde você deseja salvar o arquivo
caminho_saida = r"C:\Users\andrey.cunha\Downloads\baixaArquivo_modificado.xlsx"

# Exportar o DataFrame para um arquivo Excel
colunas_selecionadas.to_excel(caminho_saida, index=False)

print(f"Arquivo salvo em: {caminho_saida}")
print(colunas_selecionadas)
print(df_protheus)
