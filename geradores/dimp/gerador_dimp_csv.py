import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import csv

# --- Configurações do Usuário ---
# NOME DO SEU ARQUIVO DE CNPJs
ARQUIVO_CNPJS = '../cnpjs/cnpjs_ficticios.csv' # <--- CAMINHO CORRIGIDO

# PERÍODO DAS TRANSAÇÕES
MES = 8
ANO = 2025
meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

# É uma boa prática ajustar a saída para ser relativa à pasta do script
ARQUIVO_SAIDA = f'dados/transacoes-{meses[MES-1]}-{ANO}.csv'


# PERFIS DE TRANSAÇÕES POR CNAE (MODIFICADO)
# Mapeia CNAE para (min_transacoes, max_transacoes, min_valor, max_valor)
PERFIS_TRANSACOES = {
    # Alto Volume / Baixo Valor (AGORA COM MENOS TRANSAÇÕES E MAIORES VALORES)
    '7500100': (6, 14, 500.0, 2000.0), # Veterinária
    '9602502': (6, 12, 600.0, 2500.0), # Salão de Beleza
    '8650004': (4, 10, 800.0, 3000.0), # Fisioterapia
    '8630504': (6, 12, 700.0, 2800.0), # Odontologia
    '9313100': (8, 16, 400.0, 1800.0), # Academia
    '5611201': (10, 20, 300.0, 1500.0),  # Restaurante
    '4711302': (8, 16, 500.0, 2000.0), # Comércio
    '4713401': (8, 16, 550.0, 2200.0), # E-commerce
    
    # Baixo Volume / Alto Valor (agora com valores ainda maiores)
    '6201501': (2, 6, 5000.0, 50000.0), # TI/Software
    '4930202': (2, 4, 8000.0, 80000.0), # Transporte
    '6920601': (2, 6, 2000.0, 20000.0), # Contabilidade
    '7020400': (2, 4, 5000.0, 100000.0), # Consultoria
    '4120400': (1, 2, 10000.0, 200000.0), # Engenharia/Construção
    '7319002': (4, 10, 1000.0, 10000.0), # Marketing
    '8599604': (4, 8, 800.0, 8000.0), # Treinamento
}

# DADOS DO ADQUIRENTE E FORMAS DE PAGAMENTO
ADQUIRENTES = [
    {'cnpj': '12345678000190', 'nome': 'PAGBANK'},
    {'cnpj': '30000000000100', 'nome': 'STONE'},
    {'cnpj': '01000000000100', 'nome': 'CIELO'},
    {'cnpj': '04000000000100', 'nome': 'REDE'},
    {'cnpj': '05000000000100', 'nome': 'SUMUP'},
]

FORMAS_PAGAMENTO = ['CARTÃO DE DÉBITO', 'CARTÃO DE CRÉDITO', 'PIX']

# --- Fim das Configurações ---

fake = Faker('pt_BR')
transacoes_data = []

try:
    df_cnpjs = pd.read_csv(ARQUIVO_CNPJS, sep=';', encoding='utf-8')
except FileNotFoundError:
    print(f"Erro: O arquivo '{ARQUIVO_CNPJS}' não foi encontrado.")
    exit()

data_inicio_periodo = datetime(ANO, MES, 1).date()
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

        # O CEP agora é gerado sem o hífen para evitar o erro no banco de dados
        cep = fake.postcode().replace('-', '')

        transacao = {
            "CNPJ_Adquirente": adquirente_aleatorio['cnpj'],
            "Nome_Adquirente": adquirente_aleatorio['nome'],
            "Periodo_Inicio": periodo_inicio_str,
            "Periodo_Fim": periodo_fim_str,
            "CNPJ_Estabelecimento": cnpj_estab,
            "Nome_Estabelecimento": nome_estab,
            "Logradouro": fake.street_address(),
            "CEP": cep,  # Variável CEP corrigida
            "Cod_Municipio": str(random.randint(1000000, 9999999)),
            "UF": fake.state_abbr(),
            "Razao_Social": razao_social,
            "Campo_Vazio1": None, "Campo_Vazio2": None, "Data_Abertura_Estab": data_abertura,
            "Campo_Vazio3": None, "Campo_Vazio4": None, "Campo_Vazio5": data_situacao,  # Adicionado a data de situação
            "Campo_Vazio6": None,
            "Cod_CNAE": cnae,  # CORRIGIDO: Usa a variável 'cnae' ao invés do valor fixo -2
            "Cod_Subclasse": -2,
            "Campo_Vazio7": None, "Campo_Vazio8": None, "Campo_Vazio9": None,
            "Data_Transacao": data_transacao_str,
            "Data_Pagamento": data_transacao_str,
            "CNPJ_Adquirente_Repetido": adquirente_aleatorio['cnpj'],
            "Data_Credito": (data_transacao_dt + timedelta(days=1)).strftime('%Y-%m-%d'),
            "Cod_Transacao": str(random.randint(100000000, 999999999)),
            "Cod_Autorizacao": str(random.randint(100000, 999999)),
            "Cod_Desconhecido": -2,
            "Status": 0, "Meio_Pagamento": "SERVICOS", "Hora_Transacao": hora,
            "Valor": valor,
            "Forma_Pagamento": random.choice(FORMAS_PAGAMENTO)
        }
        transacoes_data.append(transacao)

df_transacoes = pd.DataFrame(transacoes_data)
df_transacoes.to_csv(ARQUIVO_SAIDA, sep='|', index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)

print(f"Arquivo '{ARQUIVO_SAIDA}' com {len(transacoes_data)} transações gerado com sucesso!")