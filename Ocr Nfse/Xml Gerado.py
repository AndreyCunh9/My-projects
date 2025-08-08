import os
import PyPDF2
import xml.etree.ElementTree as ET

def criar_xml(texto_extraido):
    root = ET.Element("Nfse", versao="2.02")
    inf_nfse = ET.SubElement(root, "InfNfse")

    # Extrair informações do texto
    # (Você precisará ajustar este código de acordo com o formato do texto extraído)
    numero_nf = "721984"  # Exemplo
    codigo_verificacao = "461664465"  # Exemplo
    data_emissao = "2024-05-17T05:38:03"  # Exemplo
    valor_total_nota = "3511.40"  # Exemplo
    cpf_cnpj_prestador = "11137051071954"  # Exemplo
    inscricao_municipal = "91668"  # Exemplo
    razao_social = "BOTICARIO PRODUTOS DE BELEZA LTDA"  # Exemplo
    nome_fantasia = "BOTICARIO PRODUTOS DE BELEZA LTDA"  # Exemplo
    endereco_prestador = "AVENIDA RUI BARBOSA"  # Exemplo
    numero_endereco_prestador = "4110"  # Exemplo
    bairro_prestador = "PARQUE DA FONTE"  # Exemplo
    codigo_municipio_prestador = "4125506"  # Exemplo
    uf_prestador = "PR"  # Exemplo
    cep_prestador = "83050010"  # Exemplo
    telefone_prestador = "4135213400"  # Exemplo
    email_prestador = "G_CSCAPFFA@GRUPOBOTICARIO.COM.BR"  # Exemplo
    codigo_municipio_orgao_gerador = "4125506"  # Exemplo
    uf_orgao_gerador = "PR"  # Exemplo
    numero_rps = "726073"  # Exemplo
    data_emissao_rps = "2024-05-20T00:00:00"  # Exemplo
    valor_servicos = "1942.83"  # Exemplo
    valor_deducoes = "0.00"  # Exemplo
    valor_pis = "0"  # Exemplo
    valor_cofins = "0"  # Exemplo
    valor_inss = "0"  # Exemplo
    valor_ir = "0"  # Exemplo
    valor_csll = "0"  # Exemplo
    outras_retencoes = "0.00"  # Exemplo
    valor_iss = "38.86"  # Exemplo
    aliquota = "2"  # Exemplo
    desconto_incondicionado = "0"  # Exemplo
    desconto_condicionado = "0"  # Exemplo
    iss_retido = "2"  # Exemplo
    item_lista_servico = "17.08"  # Exemplo
    codigo_cnae = "774030002"  # Exemplo
    codigo_tributacao_municipio = "1708"  # Exemplo
    discriminacao = "/ EUDORA TAXA DE REMUNERACAO DE FRANQUIAS / FATURA: 0258518575/001 VENCTO: 19/06/2024 R$ 323,79 FATURA: 025 8518575/002 VENCTO: 19/07/2024 R$ 323,79 FATURA: 0258518575/003 VENCTO: 19/08/2024 R$ 323,81 FATURA: 0258 518575/004 VENCTO: 17/09/2024 R$ 323,81 FATURA: 0258518575/005 VENCTO: 17/10/2024 R$ 323,81 FATURA: 02585 18575/006 VENCTO: 18/11/2024 R$ 323,82"  # Exemplo
    codigo_municipio_tomador = "2803005"  # Exemplo
    municipio_incidencia = "SAO JOSE DOS PINHAIS"  # Exemplo
    cnpj_tomador = "08489643005979"  # Exemplo
    inscricao_municipal_tomador = ""  # Exemplo
    razao_social_tomador = "COMERCIO DE PERFUMARIA GINSENG LTDA"  # Exemplo
    endereco_tomador = "PRACA OLIMPIO CARLOS"  # Exemplo
    numero_endereco_tomador = "154"  # Exemplo
    bairro_tomador = "CENTRO"  # Exemplo
    uf_tomador = "SE"  # Exemplo
    cep_tomador = "49290000"  # Exemplo
    telefone_tomador = "8221229898"  # Exemplo
    email_tomador = "NFE.GINSENG@GRUPOGINSENG.COM.BR"  # Exemplo
    regime_especial_tributacao = "Nenhum"  # Exemplo
    optante_simples_nacional = "2"  # Exemplo

    # Preencher o XML
    chave = ET.SubElement(inf_nfse, "Chave")
    chave.text = "412550611137051071954000000000916680848964300287200000000" + numero_nf
    chave_legada = ET.SubElement(inf_nfse, "ChaveLegada")
    chave_legada.text = "nfse412550611137051071954" + numero_nf + codigo_verificacao
    numero = ET.SubElement(inf_nfse, "Numero")
    numero.text = numero_nf
    codigo_verificacao_xml = ET.SubElement(inf_nfse, "CodigoVerificacao")
    codigo_verificacao_xml.text = codigo_verificacao
    data_emissao_xml = ET.SubElement(inf_nfse, "DataEmissao")
    data_emissao_xml.text = data_emissao
    valores_nfse = ET.SubElement(inf_nfse, "ValoresNfse")
    base_calculo = ET.SubElement(valores_nfse, "BaseCalculo")
    base_calculo.text = valor_total_nota
    aliquota_xml = ET.SubElement(valores_nfse, "Aliquota")
    aliquota_xml.text = aliquota
    valor_iss_xml = ET.SubElement(valores_nfse, "ValorIss")
    valor_iss_xml = base_calculo * 0.02
    valor_iss_xml.text = valor_iss
    valor_liquido_nfse = ET.SubElement(valores_nfse, "ValorLiquidoNfse")
    valor_liquido_nfse.text = valor_total_nota
    valor_credito = ET.SubElement(inf_nfse, "ValorCredito")
    valor_credito.text = "0.00"  # Exemplo
    prestador_servico = ET.SubElement(inf_nfse, "PrestadorServico")
    identificacao_prestador = ET.SubElement(prestador_servico, "IdentificacaoPrestador")
    cpf_cnpj = ET.SubElement(identificacao_prestador, "CpfCnpj")
    cnpj = ET.SubElement(cpf_cnpj, "Cnpj")
    cnpj.text = cpf_cnpj_prestador
    inscricao_municipal_xml = ET.SubElement(identificacao_prestador, "InscricaoMunicipal")
    inscricao_municipal_xml.text = inscricao_municipal
    razao_social_xml = ET.SubElement(prestador_servico, "RazaoSocial")
    razao_social_xml.text = razao_social
    nome_fantasia_xml = ET.SubElement(prestador_servico, "NomeFantasia")
    nome_fantasia_xml.text = nome_fantasia
    endereco = ET.SubElement(prestador_servico, "Endereco")
    endereco_xml = ET.SubElement(endereco, "Endereco")
    endereco_xml.text = endereco_prestador
    numero_endereco = ET.SubElement(endereco, "Numero")
    numero_endereco.text = numero_endereco_prestador
    bairro = ET.SubElement(endereco, "Bairro")
    bairro.text = bairro_prestador
    codigo_municipio = ET.SubElement(endereco, "CodigoMunicipio")
    codigo_municipio.text = codigo_municipio_prestador
    uf = ET.SubElement(endereco, "Uf")
    uf.text = uf_prestador
    cep = ET.SubElement(endereco, "Cep")
    cep.text = cep_prestador
    contato = ET.SubElement(prestador_servico, "Contato")
    telefone = ET.SubElement(contato, "Telefone")
    telefone.text = telefone_prestador
    email = ET.SubElement(contato, "Email")
    email.text = email_prestador
    orgao_gerador = ET.SubElement(inf_nfse, "OrgaoGerador")
    codigo_municipio_orgao_gerador_xml = ET.SubElement(orgao_gerador, "CodigoMunicipio")
    codigo_municipio_orgao_gerador_xml.text = codigo_municipio_orgao_gerador

    # Informações do serviço
    servico = ET.SubElement(inf_nfse, "Servico")
    valores_servico = ET.SubElement(servico, "Valores")
    valor_servicos_xml = ET.SubElement(valores_servico, "ValorServicos")
    valor_servicos_xml.text = valor_servicos
    valor_deducoes_xml = ET.SubElement(valores_servico, "ValorDeducoes")
    valor_deducoes_xml.text = valor_deducoes
    valor_pis_xml = ET.SubElement(valores_servico, "ValorPis")
    valor_pis_xml.text = valor_pis
    valor_cofins_xml = ET.SubElement(valores_servico, "ValorCofins")
    valor_cofins_xml.text = valor_cofins
    valor_inss_xml = ET.SubElement(valores_servico, "ValorInss")
    valor_inss_xml.text = valor_inss
    valor_ir_xml = ET.SubElement(valores_servico, "ValorIr")
    valor_ir_xml.text = valor_ir
    valor_csll_xml = ET.SubElement(valores_servico, "ValorCsll")
    valor_csll_xml.text = valor_csll
    outras_retencoes_xml = ET.SubElement(valores_servico, "OutrasRetencoes")
    outras_retencoes_xml.text = outras_retencoes
    valor_iss_xml = ET.SubElement(valores_servico, "ValorIss")
    valor_iss_xml.text = "{:2f}". format(float(base_calculo.text)*0.02)
    aliquota_xml = ET.SubElement(valores_servico, "Aliquota")
    aliquota_xml.text = aliquota
    desconto_incondicionado_xml = ET.SubElement(valores_servico, "DescontoIncondicionado")
    desconto_incondicionado_xml.text = desconto_incondicionado
    desconto_condicionado_xml = ET.SubElement(valores_servico, "DescontoCondicionado")
    desconto_condicionado_xml.text = desconto_condicionado
    iss_retido_xml = ET.SubElement(servico, "IssRetido")
    iss_retido_xml.text = iss_retido
    item_lista_servico_xml = ET.SubElement(servico, "ItemListaServico")
    item_lista_servico_xml.text = item_lista_servico
    codigo_cnae_xml = ET.SubElement(servico, "CodigoCnae")
    codigo_cnae_xml.text = codigo_cnae
    codigo_tributacao_municipio_xml = ET.SubElement(servico, "CodigoTributacaoMunicipio")
    codigo_tributacao_municipio_xml.text = codigo_tributacao_municipio
    discriminacao_xml = ET.SubElement(servico, "Discriminacao")
    discriminacao_xml.text = discriminacao
    codigo_municipio_xml = ET.SubElement(servico, "CodigoMunicipio")
    codigo_municipio_xml.text = codigo_municipio
    municipio_incidencia_xml = ET.SubElement(servico, "MunicipioIncidencia")
    municipio_incidencia_xml.text = municipio_incidencia

    # Tomador
    tomador = ET.SubElement(inf_nfse, "Tomador")
    identificacao_tomador = ET.SubElement(tomador, "IdentificacaoTomador")
    cpf_cnpj_tomador = ET.SubElement(identificacao_tomador, "CpfCnpj")
    cnpj_tomador = ET.SubElement(cpf_cnpj_tomador, "Cnpj")
    cnpj_tomador.text = cnpj_tomador
    razao_social_tomador_xml = ET.SubElement(tomador, "RazaoSocial")
    razao_social_tomador_xml.text = razao_social_tomador
    endereco_tomador_xml = ET.SubElement(tomador, "Endereco")
    endereco_tomador = ET.SubElement(endereco_tomador_xml, "Endereco")
    endereco_tomador.text = endereco_tomador
    numero_endereco_tomador = ET.SubElement(endereco_tomador_xml, "Numero")
    numero_endereco_tomador.text = numero_endereco_tomador
    bairro_tomador = ET.SubElement(endereco_tomador_xml, "Bairro")
    bairro_tomador.text = bairro_tomador
    codigo_municipio_tomador_xml = ET.SubElement(endereco_tomador_xml, "CodigoMunicipio")
    codigo_municipio_tomador_xml.text = codigo_municipio_tomador
    uf_tomador = ET.SubElement(endereco_tomador_xml, "Uf")
    uf_tomador.text = uf_tomador
    cep_tomador = ET.SubElement(endereco_tomador_xml, "Cep")
    cep_tomador.text = cep_tomador
    contato_tomador = ET.SubElement(tomador, "Contato")
    telefone_tomador_xml = ET.SubElement(contato_tomador, "Telefone")
    telefone_tomador_xml.text = telefone_tomador
    email_tomador_xml = ET.SubElement(contato_tomador, "Email")
    email_tomador_xml.text = email_tomador

    # Prestador
    prestador_xml = ET.SubElement(inf_nfse, "Prestador")
    cpf_cnpj_prestador_xml = ET.SubElement(prestador_xml, "CpfCnpj")
    cnpj_prestador_xml = ET.SubElement(cpf_cnpj_prestador_xml, "Cnpj")
    cnpj_prestador_xml.text = cpf_cnpj_prestador
    inscricao_municipal_prestador_xml = ET.SubElement(prestador_xml, "InscricaoMunicipal")
    inscricao_municipal_prestador_xml.text = inscricao_municipal

    # Regime Especial Tributação
    regime_especial_tributacao_xml = ET.SubElement(inf_nfse, "RegimeEspecialTributacao")
    regime_especial_tributacao_xml.text = regime_especial_tributacao

    # Optante Simples Nacional
    optante_simples_nacional_xml = ET.SubElement(inf_nfse, "OptanteSimplesNacional")
    optante_simples_nacional_xml.text = optante_simples_nacional

    # Finalizando e retornando o XML
    inf_declaracao_prestacao_servico = ET.SubElement(inf_nfse, "InfDeclaracaoPrestacaoServico")

    # Concluir o XML
    xml_string = ET.tostring(root, encoding="unicode", method="xml")
    return xml_string


def ler_pdf_e_criar_xml(pasta):
    # Verifica se a pasta existe
    if not os.path.exists(pasta):
        print(f"A pasta '{pasta}' não existe.")
        return

    # Loop pelos arquivos na pasta
    for arquivo in os.listdir(pasta):
        # Verifica se o arquivo é um PDF
        if arquivo.lower().endswith('.pdf'):
            # Caminho completo do arquivo PDF
            caminho_pdf = os.path.join(pasta, arquivo)

            # Cria um leitor PDF
            leitor_pdf = PyPDF2.PdfFileReader(open(caminho_pdf, 'rb'))

            # Extrai o texto de todas as páginas
            texto_pdf = ''
            for pagina in range(leitor_pdf.numPages):
                texto_pdf += leitor_pdf.getPage(pagina).extractText()

            # Cria o XML com base no texto extraído
            xml_resultante = criar_xml(texto_pdf)

            # Nome do arquivo XML
            nome_arquivo_xml = f"{os.path.splitext(arquivo)[0]}.xml"

            # Caminho completo do arquivo XML
            caminho_xml = os.path.join(pasta, nome_arquivo_xml)

            # Escreve o XML no arquivo
            with open(caminho_xml, 'w', encoding='utf-8') as xml_file:
                xml_file.write(xml_resultante)

            print(f"XML gerado para o arquivo PDF '{arquivo}' em '{caminho_xml}'.")


# Pasta onde os arquivos PDF estão localizados
pasta_pdf = r"C:\Users\andrey.cunha\Downloads\ND"

# Chama a função para ler os PDFs e criar os XMLs
ler_pdf_e_criar_xml(pasta_pdf)