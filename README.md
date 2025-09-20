## Geradores de Dados Fictícios para Análise Fiscal

Este projeto é um conjunto de scripts em Python para gerar dados fictícios e interconectados de CNPJs, transações DIMP, notas fiscais e declarações PGDAS. O objetivo é criar um dataset coerente para simular cenários de análise fiscal e auditoria.

---

## Tabela de Conteúdo
- [Tecnologias e Dependências](#tecnologias-e-dependências)
- [Visão Geral do Fluxo de Dados](#visão-geral-do-fluxo-de-dados)
- [Como Usar](#como-usar)
- [Análise de Dados e Próximos Passos](#análise-de-dados-e-próximos-passos)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## Tecnologias e Dependências

Este projeto foi desenvolvido em **Python**. As bibliotecas a seguir são necessárias e podem ser instaladas via pip:

```bash
pip install pandas faker numpy
```

---

## Visão Geral do Fluxo de Dados

Os scripts funcionam como um pipeline, onde a saída de um é a entrada do próximo. Isso garante a consistência e interligação dos dados gerados, simulando um ambiente de produção.

`CNPJ -> DIMP -> Notas Fiscais -> PGDAS`

---

## Como Usar

#### 1. Gerar CNPJs
Cria um arquivo CSV com 300 CNPJs base, que serão usados nos próximos passos.

```bash
python scripts/gerador_cnpj_csv.py
```

#### 2. Gerar Dados DIMP (Transações Financeiras)
Lê a lista de CNPJs e gera um arquivo com transações financeiras simulando uma DIMP, com valores distribuídos por CNAE. **Lembre-se de ajustar o MÊS e o ANO no script**.

```bash
python scripts/gerador_dimp_csv.py
```

#### 3. Gerar Notas Fiscais de Serviço

Usa os dados DIMP gerados no passo anterior para criar notas fiscais com valores que podem ter divergências, simulando cenários reais de auditoria. **Ajuste o MÊS e o ANO no script**.

```bash
python scripts/gerador_notas_xlsx.py
```

#### 4. Gerar PGDAS

Consolida os dados das notas fiscais e DIMP para gerar um arquivo PGDAS, também com cenários de divergência. *Ajuste o MÊS e o ANO no script*.

```bash
python scripts/gerador_pgdas_txt.py
```

---

## Análise de Dados e Próximos Passos

Agora que você tem os arquivos, o próximo passo é a análise! Você pode usar um script em Python (com bibliotecas como Pandas ou Polars) ou uma ferramenta de Business Intelligence (como PowerBI ou Tableau) para cruzar os dados de DIMP, Notas Fiscais e PGDAS para encontrar as divergências.

---

## Contribuição

Contribuições são bem-vindas! Se tiver sugestões ou encontrar algum problema, sinta-se à vontade para abrir uma issue ou um pull request.

---
## Licença
Este projeto está sob a Licença [MIT](https://choosealicense.com/licenses/mit/). Para mais detalhes, veja o arquivo `LICENSE`.