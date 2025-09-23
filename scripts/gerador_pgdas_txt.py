import pandas as pd
from faker import Faker
import random
from datetime import datetime
import os
import zipfile

# --- Configurações do Usuário ---
MES_COMPETENCIA = 2
ANO_COMPETENCIA = 2024
meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

# Caminhos dos arquivos de entrada
ARQUIVO_NOTAS_FISCAIS = f'../data/generated/{ANO_COMPETENCIA}/notas_fiscais/notas_fiscais_ficticias-{meses[MES_COMPETENCIA-1]}-{ANO_COMPETENCIA}.xlsx'
ARQUIVO_DIMP = f'../data/generated/{ANO_COMPETENCIA}/dimp/transacoes-{meses[MES_COMPETENCIA-1]}-{ANO_COMPETENCIA}.csv'

# Cenários de divergência
CENARIOS_PGDAS = {
    'PGDAS_IGUAL_NOTAS': 1.0,
    'NOTAS_MAIOR_PGDAS_LEVE': 0.85,
    'PGDAS_MAIOR_NOTAS_LEVE': 1.15,
    'NOTAS_MAIOR_PGDAS_RADICAL': 0.10,
    'PGDAS_MAIOR_NOTAS_RADICAL': 2.50,
}
# --- Fim das Configurações ---

fake = Faker('pt_BR')
records = []
total_records = 0

try:
    df_notas = pd.read_excel(ARQUIVO_NOTAS_FISCAIS)
    df_dimp = pd.read_csv(ARQUIVO_DIMP, sep='|', encoding='utf-8')
except FileNotFoundError as e:
    print(f"Erro: Um dos arquivos de entrada não foi encontrado. Por favor, gere os scripts anteriores primeiro. Erro: {e}")
    exit()

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
    record_00000 = f"00000|{cnpj}|{fake.numerify('##############')}|{cnpj}|{data_geracao}|2.2.23|{cnpj}|{fake.company()}|9129|S|{fake.date_object().strftime('%Y%m%d')}|{ANO_COMPETENCIA}{MES_COMPETENCIA:02}|{valor_pgdas:.2f}||A|0||0,00|0,00|||0|{fake.ipv4()}|{fake.mac_address().replace(':', '')}"
    records.append(record_00000)
    
    total_records += 3
    records.append(f"01500|{ANO_COMPETENCIA}{MES_COMPETENCIA:02}|{valor_pgdas:.2f}".replace('.', ','))
    records.append(f"01501|{ANO_COMPETENCIA}{MES_COMPETENCIA:02}|{valor_pgdas:.2f}".replace('.', ','))
    records.append(f"01502|{ANO_COMPETENCIA}{MES_COMPETENCIA:02}|0,00")

    for i in range(1, 12):
        mes_outros = MES_COMPETENCIA + i
        ano_outros = ANO_COMPETENCIA
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

PASTA_SAIDA = os.path.join('../data/generated', str(ANO_COMPETENCIA), 'pgdas')
ARQUIVO_TXT_SAIDA = f'pgdas-{meses[MES_COMPETENCIA-1]}-{ANO_COMPETENCIA}.txt'
ARQUIVO_ZIP_SAIDA = f'pgdas-{meses[MES_COMPETENCIA-1]}-{ANO_COMPETENCIA}.zip'

os.makedirs(PASTA_SAIDA, exist_ok=True)

caminho_saida_txt = os.path.join(PASTA_SAIDA, ARQUIVO_TXT_SAIDA)
with open(caminho_saida_txt, 'w', encoding='utf-8') as f:
    for line in records:
        f.write(line + '\n')

# Criar o arquivo ZIP
caminho_saida_zip = os.path.join(PASTA_SAIDA, ARQUIVO_ZIP_SAIDA)
with zipfile.ZipFile(caminho_saida_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(caminho_saida_txt, os.path.basename(caminho_saida_txt))

print(f"Arquivo '{caminho_saida_txt}' com {total_records} registros gerado com sucesso!")
print(f"Arquivo '{caminho_saida_zip}' gerado com sucesso!")
