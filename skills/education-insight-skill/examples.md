# Exemplos de Utilização

## Exemplo 1

### Entrada

```yaml
countries:
  - BRA
  - CHL
  - ARG
  - USA
  - FIN

indicator:
  - SE.XPD.TOTL.GD.ZS

period:
  start_year: 2000
  end_year: 2020
```

### Saída Esperada

```text
Resumo Executivo

O conjunto de países apresenta diferenças relevantes no investimento em educação ao longo do período analisado.

Comparação entre Países

• Brasil apresentou ...
• Chile apresentou ...
• Finlândia apresentou ...

Ranking

1. ...
2. ...
3. ...

Principais Insights

...

Recomendações

...

Limitações

...
```

---

## Exemplo 2

### Entrada

```yaml
countries:
  - BRA
  - USA

indicator:
  - SE.ADT.LITR.ZS

period:
  start_year: 2010
  end_year: 2020
```

### Saída Esperada

```text
Resumo Executivo

A comparação demonstra diferenças reduzidas entre os países para o indicador analisado.

Principais Insights

...

Recomendações

...
```