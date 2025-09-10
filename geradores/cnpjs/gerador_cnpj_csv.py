import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Configurar o gerador de dados (Faker) para o Brasil
fake = Faker('pt_BR')

# Mapear perfis de negócios com palavras-chave e CNAEs
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
    
    # NOVOS CNAEs
    {'tipo': 'Contabilidade', 'palavras_chave': ['Contábil', 'Escritório Contabilidade', 'Assessoria Fiscal'], 'cnae': '6920601', 'descricao_cnae': 'Atividades de contabilidade'},
    {'tipo': 'Consultoria', 'palavras_chave': ['Consultoria', 'Gestão', 'Estratégica', 'Negócios'], 'cnae': '7020400', 'descricao_cnae': 'Atividades de consultoria em gestão empresarial'},
    {'tipo': 'Engenharia/Construção', 'palavras_chave': ['Construção', 'Engenharia', 'Obras'], 'cnae': '4120400', 'descricao_cnae': 'Construção de edifícios'},
    {'tipo': 'Marketing', 'palavras_chave': ['Marketing', 'Publicidade', 'Agência', 'Promoção'], 'cnae': '7319002', 'descricao_cnae': 'Promoção de vendas'},
    {'tipo': 'Treinamento', 'palavras_chave': ['Treinamento', 'Desenvolvimento', 'Cursos'], 'cnae': '8599604', 'descricao_cnae': 'Treinamento em desenvolvimento profissional e gerencial'},
    {'tipo': 'E-commerce', 'palavras_chave': ['e-commerce', 'Online', 'Vendas Online', 'Comércio Digital'], 'cnae': '4713401', 'descricao_cnae': 'Lojas de departamentos ou magazines'}
]

# Função para gerar um CNPJ fictício
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

# Lista para armazenar os dados
dados = []

# Gerar 300 registros
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

# Criar o DataFrame e exportar para CSV
df = pd.DataFrame(dados)
df.to_csv('cnpjs/cnpjs_ficticios.csv', index=False, sep=';', encoding='utf-8')

print("Arquivo 'cnpjs_ficticios.csv' gerado com sucesso!")