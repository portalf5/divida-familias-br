# Endividamento das famílias segue perto do recorde após 20 anos de alta estrutural

**Reportagem de dados interativa — Portal F5**
Por Wederson Marinho · Jornalista e cientista de dados

Indicador oficial do Banco Central do Brasil mostra que o endividamento das famílias com o sistema financeiro, excluindo crédito habitacional, permanece próximo do maior nível da série histórica após duas décadas de avanço estrutural.

**Acesse a reportagem:** https://portalf5.github.io/divida-familias-br

---

## Visão geral

Este projeto combina jornalismo econômico, transparência metodológica e ciência de dados para analisar a evolução do endividamento das famílias brasileiras a partir de dados públicos oficiais do Banco Central.

A série SGS 29038 mede o endividamento das famílias como proporção da renda bruta disponível acumulada nos últimos 12 meses, excluindo o crédito habitacional. Essa delimitação torna o indicador especialmente útil para observar o comportamento do crédito ao consumo: cartão de crédito, crédito pessoal, consignado, financiamento de veículos e demais modalidades bancárias não imobiliárias.

---

## O que significa o percentual

O indicador não representa a parcela mensal da renda comprometida com prestações, nem o total de inadimplência. Ele expressa, em nível agregado nacional, a relação entre o estoque das dívidas das famílias no sistema financeiro — exceto imobiliário — e a renda bruta disponível acumulada em 12 meses.

Em termos diretos: as dívidas bancárias das famílias equivalem a cerca de 31% da renda anual disponível medida pelo Banco Central.

---

## Principais achados

| Indicador | Valor |
|---|---|
| Último dado disponível | 31,27% (jan/2026) |
| Máximo histórico | 31,54% (out/2022) |
| Mínimo histórico | 13,84% (jan/2005) |
| Variação acumulada | +17,43 p.p. desde jan/2005 |
| Média histórica | 25,03% |
| Mediana histórica | 24,83% |

---

## Fontes de dados

### Série principal

| Código | Fonte | Descrição |
|---|---|---|
| SGS 29038 | Banco Central do Brasil | Endividamento das famílias / SFN exceto crédito habitacional |

Unidade: % da renda bruta disponível acumulada nos últimos 12 meses (RNDBF)
Periodicidade: mensal · Início: janeiro de 2005
Tempestividade: até 8 semanas após o mês de referência

API pública: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.29038/dados?formato=json`
Portal: [dadosabertos.bcb.gov.br](https://dadosabertos.bcb.gov.br/dataset/29038-endividamento-das-familias-com-o-sistema-financeiro-nacional-exceto-credito-habitacional-em-r)

### Séries auxiliares

| Código | Descrição |
|---|---|
| SGS 4189 | Taxa Selic acumulada no mês (% ao ano) |
| SGS 433 | IPCA — variação mensal (%) |
| SGS 24369 | Taxa de desocupação — PNAD Contínua (%) |

---

## Metodologia

**Decomposição de tendência:** STL — Seasonal-Trend decomposition via Loess (Cleveland et al., 1990, *Journal of Official Statistics*, v. 6, n. 1). Parâmetros: `period=12, robust=True`. Implementado com `statsmodels`. Fallback: média móvel centrada de 12 meses.

**Correlações:** coeficiente r de Pearson com defasagens de 0, 1, 3 e 6 meses. Implementado com `scipy.stats.pearsonr`. Critério de significância: p < 0,05 (bicaudal).

As correlações expressam associação estatística entre séries temporais. Não inferir causalidade sem modelo econométrico estrutural adicional.

---

## Estrutura do repositório

```
divida-familias-br/
├── index.html        # reportagem (GitHub Pages)
├── data/
│   └── dados.json    # gerado pelo script Python
├── scripts/
│   └── coletar.py    # pipeline de coleta, análise e exportação
└── README.md
```

## Stack

Python · Pandas · Statsmodels · SciPy · GitHub Pages · API pública do Banco Central

---

## Como reproduzir

```bash
pip install pandas requests statsmodels scipy
python scripts/coletar.py
```

O script coleta as séries via API do BCB, executa a decomposição STL, calcula as correlações e exporta `data/dados.json`. A página lê esse arquivo automaticamente; sem ele, busca os dados diretamente da API.

---

## Identificação e citação

Marinho, Wederson. **Endividamento das famílias segue perto do recorde após 20 anos de alta estrutural.** Portal F5, 2026. Disponível em: https://portalf5.github.io/divida-familias-br

Dados primários: Banco Central do Brasil. Série SGS 29038. Dados públicos conforme política oficial de acesso e transparência do BCB.

---

## Licenças

**Dados:** públicos do Banco Central do Brasil, conforme política oficial de dados abertos e transparência.
**Código:** MIT License.

---

## Portal F5

Jornalismo econômico e de dados com foco em clareza, contexto e independência editorial.
