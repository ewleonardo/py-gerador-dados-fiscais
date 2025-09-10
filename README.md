# Geradores-Dados-Python

Este repositório contém scripts em Python para geração de dados fictícios. Os scripts são úteis para testes, desenvolvimento e preenchimento de bases de dados.

---

### Requisitos

Para usar os scripts, você precisa ter o **Python 3.6** ou superior.
Instale as bibliotecas necessárias com o comando abaixo:

```bash
pip install pandas openpyxl faker

---

### Como Usar

#### 1. Gerador de CNPJs
Este script (geradores/cnpjs/gerador_cnpj.py) cria um arquivo CSV chamado cnpjs_ficticios.csv com dados fictícios de empresas.

Passo a passo:
1. Navegue até a pasta do script:
cd geradores/cnpjs
2. Execute o script:
python gerador_cnpj.py
Saída: O arquivo cnpjs_ficticios.csv será criado na pasta geradores/cnpjs/.

---

#### 2. Gerador de Transações DIMP
Este script (geradores/dimp/gerador_dimp.py) cria um arquivo CSV de transações fictícias no formato DIMP. Ele **depende** do arquivo de CNPJs, então você deve rodar o primeiro script antes.

Passo a passo:
1. Navegue até a pasta do script:
cd geradores/dimp
2. Execute o script:
python gerador_dimp.py
Configuração: Você pode alterar o mês e o ano das transações diretamente no script, nas variáveis MES e ANO.
Saída: O arquivo transacoes-MES-ANO.csv será criado na pasta geradores/dimp/dados/.

---

### Licença

Este projeto está sob a Licença MIT.