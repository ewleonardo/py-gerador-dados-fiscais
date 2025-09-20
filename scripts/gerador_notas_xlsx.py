import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import numpy as np

# --- Configurações do Usuário ---
MES_COMPETENCIA = 1
ANO_COMPETENCIA = 2025
meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

# Caminho do arquivo DIMP
ARQUIVO_DIMP = f'../data/generated/{ANO_COMPETENCIA}/dimp/transacoes-{meses[MES_COMPETENCIA-1]}-{ANO_COMPETENCIA}.csv'

# Cenários de divergência entre DIMP e Notas Fiscais
CENARIOS = {
    'NOTAS_IGUAL_DIMP': 1.0,
    'DIMP_MAIOR_NOTAS_LEVE': 0.85,
    'NOTAS_MAIOR_DIMP_LEVE': 1.15,
    'DIMP_MAIOR_NOTAS_RADICAL': 0.40,
    'NOTAS_MAIOR_DIMP_RADICAL': 2.50,
}
# --- Fim das Configurações ---

fake = Faker('pt_BR')
servicos_data = []

# Mapeamento de CNAE para Atividade
ATIVIDADES_MAP = {
    '7500100': '404', '9602502': '404', '8650004': '404',
    '8630504': '404', '9313100': '404', '6201501': '404',
    '5611201': '402', '4711302': '402', '4930202': '404',
    '6920601': '404', '7020400': '404', '4120400': '404',
    '7319002': '404', '8599604': '404', '4713401': '404'
}

# Carrega os dados DIMP
try:
    df_dimp = pd.read_csv(ARQUIVO_DIMP, sep='|', encoding='utf-8')
except FileNotFoundError:
    print(f"Erro: O arquivo '{ARQUIVO_DIMP}' não foi encontrado. Por favor, gere-o primeiro.")
    exit()

# Agrupa por CNPJ para gerar notas com valores coerentes
df_agrupado = df_dimp.groupby('CNPJ_Estabelecimento').agg(
    total_valor=('Valor', 'sum'),
    cnae_fiscal=('Cod_CNAE', 'first')
).reset_index()

# Geração das notas fiscais para cada CNPJ
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
        data_emissao = fake.date_between(start_date=datetime(ANO_COMPETENCIA, MES_COMPETENCIA, 1), end_date=datetime(ANO_COMPETENCIA, MES_COMPETENCIA, 28))
        local_incidencia = f'{fake.city()} - {fake.state_abbr()}'
        base_calculo = valor_nota
        aliquota = 3.0
        valor_iss = round(base_calculo * (aliquota / 100), 2)
        
        registro = {
            'PRESTADOR': cnpj_prestador, 'TOMADOR': tomador_nome, 'NÚMERO': numero_nota,
            'MÊS COMPETÊNCIA': MES_COMPETENCIA, 'ANO COMPETÊNCIA': ANO_COMPETENCIA,
            'DATA EMISSÃO': data_emissao.strftime('%Y-%m-%d'), 'SITUAÇÃO': 'Normal',
            'ISS RETIDO': 'N', 'VALOR SERVIÇOS': valor_nota, 'VALOR DESCONTO': 0.0,
            'BASE DE CÁLCULO': base_calculo, 'VALOR TOTAL': valor_nota,
            'ALÍQUOTA': aliquota, 'VALOR ISS': valor_iss,
            'LOCAL INCIDÊNCIA': local_incidencia,
            'ATIVIDADE': ATIVIDADES_MAP.get(cnae_prestador, '404')
        }
        servicos_data.append(registro)

# Cria e salva o arquivo de notas fiscais
df_servicos = pd.DataFrame(servicos_data)
PASTA_SAIDA = os.path.join('../data/generated', str(ANO_COMPETENCIA), 'notas_fiscais')
ARQUIVO_SAIDA = f'notas_fiscais_ficticias-{meses[MES_COMPETENCIA-1]}-{ANO_COMPETENCIA}.xlsx'
os.makedirs(PASTA_SAIDA, exist_ok=True)
caminho_completo_saida = os.path.join(PASTA_SAIDA, ARQUIVO_SAIDA)

try:
    df_servicos.to_excel(caminho_completo_saida, index=False, sheet_name='Notas', float_format="%.2f")
    print(f"Arquivo '{caminho_completo_saida}' com {len(df_servicos)} registros gerado com sucesso!")
except Exception as e:
    print(f"Erro ao salvar o arquivo Excel: {e}")