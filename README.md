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
pip install pandas faker numpy openpyxl
```

---

## Visão Geral do Fluxo de Dados

O projeto é estruturado como um pipeline, onde a saída de um script serve como entrada para o próximo, garantindo a consistência dos dados.

```bash
CNPJs -> DIMP -> Notas Fiscais -> PGDAS (TXT + ZIP)
```

O fluxo principal é orquestrado de forma automatizada, mas os scripts individuais também podem ser executados para cenários específicos.

---

## Como Usar

### Método Automatizado (Recomendado)

O script `main.py` automatiza todo o processo de geração para um período de anos.

#### 1.  Acesse o diretório `scripts`.
```bash
cd scripts
```

#### 2.  Execute o script principal.
```bash
python main.py
```

##### 3.  Insira o **ano inicial** e o **ano final** quando solicitado. O script irá gerar os CNPJs (uma única vez) e, em seguida, os arquivos DIMP, notas fiscais e PGDAS para cada mês do período.

### Método Manual (Para cenários específicos)

Para gerar dados de forma individual, siga os passos abaixo:

#### 1.  **Gerar CNPJs**
```bash
python scripts/gerador_cnpj_csv.py
```

#### 2.  **Gerar Dados DIMP (Transações Financeiras)**
```bash
python scripts/gerador_dimp_csv.py
```

#### 3.  **Gerar Notas Fiscais de Serviço**
```bash
python scripts/gerador_notas_xlsx.py
```

#### 4.  **Gerar PGDAS**
```bash
python scripts/gerador_pgdas_txt.py
```

**Observação:** Ao usar o método manual, lembre-se de ajustar o `MES_COMPETENCIA` e o `ANO_COMPETENCIA` em cada script.

---

## Análise de Dados e Próximos Passos

Agora que você tem os arquivos, o próximo passo é a análise! Você pode usar um script em Python (com bibliotecas como Pandas ou Polars) ou uma ferramenta de Business Intelligence (como PowerBI ou Tableau) para cruzar os dados de DIMP, Notas Fiscais e PGDAS para encontrar as divergências.

---

## Contribuição

Contribuições são bem-vindas! Se tiver sugestões ou encontrar algum problema, sinta-se à vontade para abrir uma issue ou um pull request.

---
## Licença
Este projeto está sob a Licença [MIT](https://choosealicense.com/licenses/mit/). Para mais detalhes, veja o arquivo `LICENSE`.