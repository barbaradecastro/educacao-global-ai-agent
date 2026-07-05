# Workflow n8n

## Visão Geral

Este diretório contém o workflow desenvolvido em **n8n** para automatizar a execução do projeto **Global Education AI Agent**.

O objetivo do workflow é simplificar a utilização da solução, permitindo que o pipeline seja executado de forma organizada e integrada, desde o processamento dos dados até a geração da análise executiva.

---

# Fluxo de Execução

O workflow é composto pelas seguintes etapas:

1. **Gatilho**
  - Inicia a execução do fluxo de forma periódica utilizando o Schedule Trigger.
   - O exemplo está configurado para execução semanal.

2. **Execução do Pipeline Python**
   - Executa o comando responsável por iniciar todo o pipeline de processamento dos dados.

3. **Leitura dos Resultados**
   - Lê o arquivo `final_analysis.json` gerado pelo pipeline.

4. **Análise com Inteligência Artificial**
   - Envia os dados processados para a OpenAI, responsável pela geração de uma análise executiva em linguagem natural.

5. **Armazenamento do Resultado**
   - Salva a análise produzida em um novo arquivo Markdown na pasta `reports/`.

---

# Estrutura do Workflow

```text
Manual Trigger
      │
      ▼
Execute Python Pipeline
      │
      ▼
Read Final Analysis JSON
      │
      ▼
OpenAI Executive Analysis
      │
      ▼
Write n8n Report
```

---

# Requisitos

Antes de executar o workflow é necessário:

- Python 3.12 ou superior;
- dependências instaladas (`requirements.txt`);
- dataset EdStats disponível na pasta `data/raw`;
- credencial da OpenAI configurada no n8n (opcional para geração da análise executiva).

---

# Arquivo do Workflow

O workflow está disponível em:

```text
workflow.json
```

Esse arquivo pode ser importado diretamente no n8n.

---

# Observações

A integração com a OpenAI é opcional.

Caso a credencial da API não esteja configurada, o pipeline Python poderá ser executado normalmente utilizando o parâmetro:

```bash
python -m src.main --skip-openai
```

Nesse cenário, todas as etapas de processamento, métricas, rankings, comparações, gráficos e relatórios continuam sendo geradas normalmente, exceto a análise executiva produzida pela IA.

---

# Objetivo

O workflow foi desenvolvido para demonstrar como ferramentas de orquestração podem ser utilizadas para integrar processamento de dados, Inteligência Artificial e geração automática de relatórios em um único fluxo de execução.