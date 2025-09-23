import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import csv
import numpy as np
import zipfile

# --- Configurações globais ---
fake = Faker('pt_BR')
meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
PASTA_RAIZ = '../data'
PASTA_CNPJS = os.path.join(PASTA_RAIZ, 'cnpjs')
ARQUIVO_CNPJS = os.path.join(PASTA_CNPJS, 'cnpjs_ficticios.csv')
# --- Fim das Configurações ---

# --- Funções auxiliares para gerar dados fictícios ---
def gerar_cnpj_ficticio():
    return fake.cnpj().replace('.', '').replace('/', '').replace('-', '')

def gerar_nome_empresa(perfil):
    palavra_chave = random.choice(perfil['palavras_chave'])
    nome_socio = fake.first_name()
    opcoes_nome = [
        f'{palavra_chave} {fake.last_name()} {random.choice(["LTDA", "S.A."])}',
        f'{nome_socio} {palavra_chave} {random.choice(["LTDA", "EIRELI"])}',
        f'Comércio e Serviços de {palavra_chave} {random.choice(["EIRELI", "S.A."])}',
    ]
    return random.choice(opcoes_nome)

def gerar_data_atividade():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 5)
    return fake.date_between(start_date=start_date, end_date=end_date).strftime('%d/%m/%Y')

def gerar_simples_mei():
    simples = random.choice(['SIM', 'NÃO'])
    mei = 'SIM' if simples == 'SIM' and random.random() < 0.3 else 'NÃO'
    return simples, mei
# --- Fim das Funções auxiliares ---

# --- Lógica dos scripts originais convertida em funções ---
def gerar_cnpjs():
    """Gera o arquivo CSV de CNPJs fictícios."""
    perfis_negocios = [
        {'tipo': 'Veterinária', 'palavras_chave': ['Pet', 'Animal', 'Saúde Animal'], 'cnae': '7500100', 'descricao_cnae': 'Atividades veterinárias'},
        {'tipo': 'Salão de Beleza', 'palavras_chave': ['Beleza', 'Estética', 'Salão', 'Cabelo & Corpo'], 'cnae': '9602502', 'descricao_cnae': 'Atividades de estética e outros serviços de cuidados com a beleza'},
        {'tipo': 'Fisioterapia', 'palavras_chave': ['Fisio', 'Corpo', 'Movimento', 'Saúde'], 'cnae': '8650004', 'descricao_cnae': 'Atividades de fisioterapia'},
        {'tipo': 'Odontologia', 'palavras_chave': ['Odonto', 'Sorriso', 'Clínica Odontológica'], 'cnae': '8630504', 'descricao_cnae': 'Atividade odontológica'},
        {'tipo': 'Academia', 'palavras_chave': ['Fitness', 'Academia', 'Treino', 'Corpo e Mente'], 'cnae': '9313100', 'descricao_cnae': 'Atividades de condicionamento físico'},
        {'tipo': 'TI/Software', 'palavras_chave': ['Software', 'Tecnologia', 'Sistemas', 'Inovação'], 'cnae': '6201501', 'descricao_cnae': 'Desenvolvimento de programas de computador'},
        {'tipo': 'Restaurante', 'palavras_chave': ['Restaurante', 'Lanchonete', 'Alimentos', 'Sabores'], 'cnae': '5611201', 'descricao_cnae': 'Restaurantes e similares'},
        {'tipo': 'Comércio', 'palavras_chave': ['Comercial', 'Varejo', 'Atacadista'], 'cnae': '4711302', 'descricao_cnae': 'Comércio varejista de mercadorias em geral'},
        {'tipo': 'Transporte', 'palavras_chave': ['Transportes', 'Logística', 'Cargas'], 'cnae': '4930202', 'descricao_cnae': 'Transporte rodoviário de carga'},
        {'tipo': 'Contabilidade', 'palavras_chave': ['Contábil', 'Escritório Contabilidade', 'Assessoria Fiscal'], 'cnae': '6920601', 'descricao_cnae': 'Atividades de contabilidade'},
        {'tipo': 'Consultoria', 'palavras_chave': ['Consultoria', 'Gestão', 'Estratégica', 'Negócios'], 'cnae': '7020400', 'descricao_cnae': 'Atividades de consultoria em gestão empresarial'},
        {'tipo': 'Engenharia/Construção', 'palavras_chave': ['Construção', 'Engenharia', 'Obras'], 'cnae': '4120400', 'descricao_cnae': 'Construção de edifícios'},
        {'tipo': 'Marketing', 'palavras_chave': ['Marketing', 'Publicidade', 'Agência', 'Promoção'], 'cnae': '7319002', 'descricao_cnae': 'Promoção de vendas'},
        {'tipo': 'Treinamento', 'palavras_chave': ['Treinamento', 'Desenvolvimento', 'Cursos'], 'cnae': '8599604', 'descricao_cnae': 'Treinamento em desenvolvimento profissional e gerencial'},
        {'tipo': 'E-commerce', 'palavras_chave': ['e-commerce', 'Online', 'Vendas Online', 'Comércio Digital'], 'cnae': '4713401', 'descricao_cnae': 'Lojas de departamentos ou magazines'}
    ]
    dados = []
    for _ in range(300):
        cnpj_limpo = gerar_cnpj_ficticio()
        cnpj_formatado = f'{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}'
        perfil = random.choice(perfis_negocios)
        razao_social = gerar_nome_empresa(perfil)
        nome_fantasia = razao_social.replace(random.choice(["LTDA", "EIRELI", "S.A."]), "").strip()
        socio = fake.name()
        data_inicio = gerar_data_atividade()
        simples, mei = gerar_simples_mei()
        registro = {
            'cpf_cnpj_clean': cnpj_limpo,
            'cpf_cnpj': cnpj_formatado,
            'nome_fantasia': nome_fantasia,
            'razao_social': razao_social,
            'data_de_inicio_atividade': data_inicio,
            'simples': simples,
            'mei': mei,
            'socios': socio,
            'cnae_fiscal': f'{perfil["cnae"]} - {perfil["descricao_cnae"]}',
            'cnae_fiscal_secundaria': 'N/D',
            'identificador_matriz_filial': 'Matriz',
            'situacao_cadastral': 'Ativa',
            'data_situacao_cadastral': data_inicio
        }
        dados.append(registro)

    df = pd.DataFrame(dados)
    os.makedirs(PASTA_CNPJS, exist_ok=True)
    df.to_csv(ARQUIVO_CNPJS, index=False, sep=';', encoding='utf-8')
    print(f"Arquivo '{ARQUIVO_CNPJS}' gerado com sucesso!")

def gerar_dimp(mes, ano):
    """Gera o arquivo CSV de transações DIMP para um dado mês e ano."""
    PASTA_SAIDA = os.path.join(PASTA_RAIZ, 'generated', str(ano), 'dimp')
    ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, f'transacoes-{meses[mes-1]}-{ano}.csv')

    PERFIS_TRANSACOES = {
        '7500100': (6, 14, 500.0, 2000.0),
        '9602502': (6, 12, 600.0, 2500.0),
        '8650004': (4, 10, 800.0, 3000.0),
        '8630504': (6, 12, 700.0, 2800.0),
        '9313100': (8, 16, 400.0, 1800.0),
        '5611201': (10, 20, 300.0, 1500.0),
        '4711302': (8, 16, 500.0, 2000.0),
        '4713401': (8, 16, 550.0, 2200.0),
        '6201501': (2, 6, 5000.0, 50000.0),
        '4930202': (2, 4, 8000.0, 80000.0),
        '6920601': (2, 6, 2000.0, 20000.0),
        '7020400': (2, 4, 5000.0, 100000.0),
        '4120400': (1, 2, 10000.0, 200000.0),
        '7319002': (4, 10, 1000.0, 10000.0),
        '8599604': (4, 8, 800.0, 8000.0),
    }

    ADQUIRENTES = [
        {'cnpj': '12345678000190', 'nome': 'PAGBANK'},
        {'cnpj': '30000000000100', 'nome': 'STONE'},
        {'cnpj': '01000000000100', 'nome': 'CIELO'},
        {'cnpj': '04000000000100', 'nome': 'REDE'},
        {'cnpj': '05000000000100', 'nome': 'SUMUP'},
    ]

    FORMAS_PAGAMENTO = ['CARTÃO DE DÉBITO', 'CARTÃO DE CRÉDITO', 'PIX']

    try:
        df_cnpjs = pd.read_csv(ARQUIVO_CNPJS, sep=';', encoding='utf-8')
    except FileNotFoundError:
        print(f"Erro: O arquivo '{ARQUIVO_CNPJS}' não foi encontrado. Execute o 'gerador_cnpjs' primeiro.")
        return

    transacoes_data = []
    data_inicio_periodo = datetime(ano, mes, 1).date()
    data_fim_periodo = (data_inicio_periodo.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    periodo_inicio_str = data_inicio_periodo.strftime('%Y-%m-%d')
    periodo_fim_str = data_fim_periodo.strftime('%Y-%m-%d')

    for _, cnpj_info in df_cnpjs.iterrows():
        cnae = cnpj_info['cnae_fiscal'].split(' - ')[0]
        parametros = PERFIS_TRANSACOES.get(cnae, (10, 30, 50.0, 500.0))
        min_transacoes, max_transacoes, min_valor, max_valor = parametros
        num_transacoes = random.randint(min_transacoes, max_transacoes)
        for _ in range(num_transacoes):
            data_transacao_dt = fake.date_between_dates(date_start=data_inicio_periodo, date_end=data_fim_periodo)
            data_transacao_str = data_transacao_dt.strftime('%Y-%m-%d')
            adquirente_aleatorio = random.choice(ADQUIRENTES)
            valor = round(random.uniform(min_valor, max_valor), 2)
            hora = fake.time()
            cnpj_estab = cnpj_info['cpf_cnpj_clean']
            nome_estab = cnpj_info['nome_fantasia']
            razao_social = cnpj_info['razao_social']
            data_abertura = datetime.strptime(cnpj_info['data_de_inicio_atividade'], '%d/%m/%Y').strftime('%Y-%m-%d')
            data_situacao = datetime.strptime(cnpj_info['data_situacao_cadastral'], '%d/%m/%Y').strftime('%Y-%m-%d')
            cep = fake.postcode().replace('-', '')
            transacao = {
                "CNPJ_Adquirente": adquirente_aleatorio['cnpj'], "Nome_Adquirente": adquirente_aleatorio['nome'],
                "Periodo_Inicio": periodo_inicio_str, "Periodo_Fim": periodo_fim_str,
                "CNPJ_Estabelecimento": cnpj_estab, "Nome_Estabelecimento": nome_estab,
                "Logradouro": fake.street_address(), "CEP": cep, "Cod_Municipio": str(random.randint(1000000, 9999999)),
                "UF": fake.state_abbr(), "Razao_Social": razao_social,
                "Campo_Vazio1": None, "Campo_Vazio2": None, "Data_Abertura_Estab": data_abertura,
                "Campo_Vazio3": None, "Campo_Vazio4": None, "Campo_Vazio5": data_situacao,
                "Campo_Vazio6": None, "Cod_CNAE": cnae, "Cod_Subclasse": -2,
                "Campo_Vazio7": None, "Campo_Vazio8": None, "Campo_Vazio9": None,
                "Data_Transacao": data_transacao_str, "Data_Pagamento": data_transacao_str,
                "CNPJ_Adquirente_Repetido": adquirente_aleatorio['cnpj'],
                "Data_Credito": (data_transacao_dt + timedelta(days=1)).strftime('%Y-%m-%d'),
                "Cod_Transacao": str(random.randint(100000000, 999999999)), "Cod_Autorizacao": str(random.randint(100000, 999999)),
                "Cod_Desconhecido": -2, "Status": 0, "Meio_Pagamento": "SERVICOS", "Hora_Transacao": hora,
                "Valor": valor, "Forma_Pagamento": random.choice(FORMAS_PAGAMENTO)
            }
            transacoes_data.append(transacao)

    df_transacoes = pd.DataFrame(transacoes_data)
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    df_transacoes.to_csv(ARQUIVO_SAIDA, sep='|', index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)
    print(f"Arquivo '{ARQUIVO_SAIDA}' com {len(transacoes_data)} transações gerado com sucesso!")


def gerar_notas(mes, ano):
    """Gera o arquivo XLSX de notas fiscais para um dado mês e ano."""
    ARQUIVO_DIMP = os.path.join(PASTA_RAIZ, 'generated', str(ano), 'dimp', f'transacoes-{meses[mes-1]}-{ano}.csv')
    PASTA_SAIDA = os.path.join(PASTA_RAIZ, 'generated', str(ano), 'notas_fiscais')
    ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, f'notas_fiscais_ficticias-{meses[mes-1]}-{ano}.xlsx')

    CENARIOS = {
        'NOTAS_IGUAL_DIMP': 1.0,
        'DIMP_MAIOR_NOTAS_LEVE': 0.85,
        'NOTAS_MAIOR_DIMP_LEVE': 1.15,
        'DIMP_MAIOR_NOTAS_RADICAL': 0.40,
        'NOTAS_MAIOR_DIMP_RADICAL': 2.50,
    }
    
    ATIVIDADES_MAP = {
        '7500100': '404', '9602502': '404', '8650004': '404',
        '8630504': '404', '9313100': '404', '6201501': '404',
        '5611201': '402', '4711302': '402', '4930202': '404',
        '6920601': '404', '7020400': '404', '4120400': '404',
        '7319002': '404', '8599604': '404', '4713401': '404'
    }

    try:
        df_dimp = pd.read_csv(ARQUIVO_DIMP, sep='|', encoding='utf-8')
    except FileNotFoundError:
        print(f"Erro: O arquivo '{ARQUIVO_DIMP}' não foi encontrado. Gere o 'gerador_dimp' primeiro.")
        return

    servicos_data = []
    df_agrupado = df_dimp.groupby('CNPJ_Estabelecimento').agg(
        total_valor=('Valor', 'sum'),
        cnae_fiscal=('Cod_CNAE', 'first')
    ).reset_index()

    for _, row in df_agrupado.iterrows():
        cnpj_prestador = row['CNPJ_Estabelecimento']
        valor_total_dimp = row['total_valor']
        cnae_prestador = str(row['cnae_fiscal'])
        cenario_escolhido = random.choice(list(CENARIOS.keys()))
        fator_ajuste = CENARIOS[cenario_escolhido]
        valor_total_notas = valor_total_dimp * fator_ajuste
        num_notas = 10
        valores_notas = [random.uniform(0.5, 1.5) for _ in range(num_notas)]
        soma_valores = sum(valores_notas)
        valores_finais = [round(v / soma_valores * valor_total_notas, 2) for v in valores_notas]
        soma_final = sum(valores_finais)
        diferenca = round(valor_total_notas - soma_final, 2)
        valores_finais[0] += diferenca
        
        for valor_nota in valores_finais:
            tomador_cnpj = fake.cnpj().replace('.', '').replace('/', '').replace('-', '')
            tomador_nome = fake.company()
            numero_nota = random.randint(1000, 99999)
            data_emissao = fake.date_between(start_date=datetime(ano, mes, 1), end_date=datetime(ano, mes, 28))
            local_incidencia = f'{fake.city()} - {fake.state_abbr()}'
            base_calculo = valor_nota
            aliquota = 3.0
            valor_iss = round(base_calculo * (aliquota / 100), 2)
            
            registro = {
                'PRESTADOR': cnpj_prestador, 'TOMADOR': tomador_nome, 'NÚMERO': numero_nota,
                'MÊS COMPETÊNCIA': mes, 'ANO COMPETÊNCIA': ano,
                'DATA EMISSÃO': data_emissao.strftime('%Y-%m-%d'), 'SITUAÇÃO': 'Normal',
                'ISS RETIDO': 'N', 'VALOR SERVIÇOS': valor_nota, 'VALOR DESCONTO': 0.0,
                'BASE DE CÁLCULO': base_calculo, 'VALOR TOTAL': valor_nota,
                'ALÍQUOTA': aliquota, 'VALOR ISS': valor_iss,
                'LOCAL INCIDÊNCIA': local_incidencia,
                'ATIVIDADE': ATIVIDADES_MAP.get(cnae_prestador, '404')
            }
            servicos_data.append(registro)

    df_servicos = pd.DataFrame(servicos_data)
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    try:
        df_servicos.to_excel(ARQUIVO_SAIDA, index=False, sheet_name='Notas', float_format="%.2f")
        print(f"Arquivo '{ARQUIVO_SAIDA}' com {len(df_servicos)} registros gerado com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o arquivo Excel: {e}")

def gerar_pgdas(mes, ano):
    """Gera o arquivo TXT de declarações PGDAS para um dado mês e ano e o compacta em um ZIP."""
    ARQUIVO_NOTAS_FISCAIS = os.path.join(PASTA_RAIZ, 'generated', str(ano), 'notas_fiscais', f'notas_fiscais_ficticias-{meses[mes-1]}-{ano}.xlsx')
    ARQUIVO_DIMP = os.path.join(PASTA_RAIZ, 'generated', str(ano), 'dimp', f'transacoes-{meses[mes-1]}-{ano}.csv')
    PASTA_SAIDA = os.path.join(PASTA_RAIZ, 'generated', str(ano), 'pgdas')
    ARQUIVO_TXT_SAIDA = f'pgdas-{meses[mes-1]}-{ano}.txt'
    ARQUIVO_ZIP_SAIDA = f'pgdas-{meses[mes-1]}-{ano}.zip'

    CENARIOS_PGDAS = {
        'PGDAS_IGUAL_NOTAS': 1.0,
        'NOTAS_MAIOR_PGDAS_LEVE': 0.85,
        'PGDAS_MAIOR_NOTAS_LEVE': 1.15,
        'NOTAS_MAIOR_PGDAS_RADICAL': 0.10,
        'PGDAS_MAIOR_NOTAS_RADICAL': 2.50,
    }
    
    try:
        df_notas = pd.read_excel(ARQUIVO_NOTAS_FISCAIS)
        df_dimp = pd.read_csv(ARQUIVO_DIMP, sep='|', encoding='utf-8')
    except FileNotFoundError as e:
        print(f"Erro: Um dos arquivos de entrada não foi encontrado. Gere os scripts anteriores primeiro. Erro: {e}")
        return

    records = []
    total_records = 0

    df_notas_agrupado = df_notas.groupby('PRESTADOR').agg(total_valor_notas=('VALOR TOTAL', 'sum')).reset_index()
    df_merged = pd.merge(df_notas_agrupado, df_dimp.groupby('CNPJ_Estabelecimento').agg(total_valor_dimp=('Valor', 'sum')).reset_index(), left_on='PRESTADOR', right_on='CNPJ_Estabelecimento', how='left')

    data_geracao = datetime.now().strftime('%Y%m%d')
    records.append(f"AAAAA|102|{data_geracao}|{data_geracao}")
    total_records += 1

    for _, row in df_merged.iterrows():
        cnpj = str(row['PRESTADOR']).replace('.0', '')
        valor_total_notas = row['total_valor_notas']
        cenario_escolhido = random.choice(list(CENARIOS_PGDAS.keys()))
        fator_ajuste = CENARIOS_PGDAS[cenario_escolhido]
        valor_pgdas = round(valor_total_notas * fator_ajuste, 2)

        total_records += 1
        record_00000 = f"00000|{cnpj}|{fake.numerify('##############')}|{cnpj}|{data_geracao}|2.2.23|{cnpj}|{fake.company()}|9129|S|{fake.date_object().strftime('%Y%m%d')}|{ano}{mes:02}|{valor_pgdas:.2f}||A|0||0,00|0,00|||0|{fake.ipv4()}|{fake.mac_address().replace(':', '')}"
        records.append(record_00000)
        
        total_records += 3
        records.append(f"01500|{ano}{mes:02}|{valor_pgdas:.2f}".replace('.', ','))
        records.append(f"01501|{ano}{mes:02}|{valor_pgdas:.2f}".replace('.', ','))
        records.append(f"01502|{ano}{mes:02}|0,00")

        for i in range(1, 12):
            mes_outros = mes + i
            ano_outros = ano
            if mes_outros > 12:
                mes_outros -= 12
                ano_outros += 1
            total_records += 3
            records.append(f"01500|{ano_outros}{mes_outros:02}|0,00")
            records.append(f"01501|{ano_outros}{mes_outros:02}|0,00")
            records.append(f"01502|{ano_outros}{mes_outros:02}|0,00")

        total_records += 1
        records.append(f"02000|{random.uniform(500, 1000):.2f}|{random.uniform(20000, 30000):.2f}|{random.uniform(500, 1000):.2f}|{random.uniform(500, 1000):.2f}|{random.uniform(20000, 30000):.2f}|||{random.uniform(20000, 30000):.2f}|{random.uniform(20000, 30000):.2f}|0,00|0,00|{random.uniform(500, 1000):.2f}|{random.uniform(500, 1000):.2f}|{random.uniform(500, 1000):.2f}|0,00|0,00|0,00".replace('.', ','))

        total_records += 1
        records.append(f"03000|{cnpj}|{fake.state_abbr()}|9129|0|{random.uniform(100000, 500000):.2f}|0,0000000000|0,0000000000|0,0000000000|0,0000000000|0")

        records_in_cnpj = 1 + 3 + (3 * 11) + 1 + 1
        records.append(f"99999|{records_in_cnpj}")
        total_records += 1

    records.append(f"ZZZZZ|{total_records}")

    os.makedirs(PASTA_SAIDA, exist_ok=True)
    caminho_saida_txt = os.path.join(PASTA_SAIDA, ARQUIVO_TXT_SAIDA)
    with open(caminho_saida_txt, 'w', encoding='utf-8') as f:
        for line in records:
            f.write(line + '\n')

    caminho_saida_zip = os.path.join(PASTA_SAIDA, ARQUIVO_ZIP_SAIDA)
    with zipfile.ZipFile(caminho_saida_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(caminho_saida_txt, os.path.basename(caminho_saida_txt))

    print(f"Arquivo '{caminho_saida_txt}' com {total_records} registros gerado com sucesso!")
    print(f"Arquivo '{caminho_saida_zip}' gerado com sucesso!")


# --- Função principal para orquestrar a geração dos dados ---
def main():
    """Função principal que executa a geração de todos os arquivos fiscais."""
    print("Iniciando a geração de dados fiscais fictícios...")

    try:
        ano_inicial = int(input("Por favor, insira o ano inicial (ex: 2021): "))
        ano_final = int(input("Por favor, insira o ano final (ex: 2025): "))
        if ano_final < ano_inicial:
            print("O ano final deve ser maior ou igual ao ano inicial.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, insira números inteiros para os anos.")
        return

    # Passo 1: Gerar o arquivo de CNPJs
    print("\nGerando CNPJs base...")
    gerar_cnpjs()

    # Passo 2: Iterar por cada ano e mês para gerar os demais arquivos
    for ano in range(ano_inicial, ano_final + 1):
        print(f"\n--- Gerando dados para o ano {ano} ---")
        for mes in range(1, 13):
            print(f"--- Mês: {meses[mes-1].capitalize()} ---")
            gerar_dimp(mes, ano)
            gerar_notas(mes, ano)
            gerar_pgdas(mes, ano)
    
    print("\nProcesso de geração de dados concluído com sucesso!")
    print(f"Os arquivos foram salvos na pasta '{os.path.abspath(os.path.join(PASTA_RAIZ, 'generated'))}'")

if __name__ == "__main__":
    main()
