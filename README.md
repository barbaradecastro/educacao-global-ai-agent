# 🌍 Global Education AI Agent

### Pipeline Inteligente para Análise Global de Indicadores Educacionais

O **Global Education AI Agent** automatiza a análise de indicadores educacionais utilizando o dataset **World Bank Education Statistics (EdStats)**. A solução implementa um pipeline completo para carregamento, tratamento, análise e geração de relatórios, permitindo transformar grandes volumes de dados em informações estratégicas para apoio à tomada de decisão.

O projeto foi desenvolvido utilizando uma arquitetura modular em **Python**, facilitando manutenção, reutilização de componentes e futuras evoluções da solução. Como diferencial, também oferece integração opcional com modelos da **OpenAI** para geração de análises executivas em linguagem natural.

---

# 🎯 Objetivos

O pipeline foi desenvolvido para:

- Automatizar o processamento do dataset World Bank Education Statistics (EdStats);
- Limpar, validar e transformar os dados para formato analítico;
- Calcular métricas estatísticas e evolução histórica dos indicadores;
- Gerar rankings e comparações entre países;
- Produzir gráficos e relatórios estruturados automaticamente;
- Disponibilizar uma arquitetura preparada para integração com Inteligência Artificial.

---

# ✨ Principais Funcionalidades

- 📥 Carregamento automático dos arquivos do EdStats;
- 🧹 Limpeza e validação dos dados;
- 🔄 Transformação para formato analítico (Long Format);
- 📊 Cálculo de métricas educacionais;
- 🏆 Geração de rankings por indicador;
- 🌎 Comparação entre países;
- 📈 Geração automática de gráficos;
- 📝 Exportação dos resultados em CSV, JSON e Markdown;
- 📑 Geração automática de relatórios;
- 🤖 Integração opcional com OpenAI;
- ✅ Testes automatizados utilizando Pytest.

---

# 🚀 Destaques da Solução

| Recurso | Status |
|----------|:------:|
| Dataset oficial World Bank EdStats | ✅ |
| Pipeline completo de processamento | ✅ |
| Arquitetura modular | ✅ |
| Métricas e rankings | ✅ |
| Comparação entre países | ✅ |
| Geração automática de gráficos | ✅ |
| Relatórios estruturados | ✅ |
| Testes automatizados | ✅ |
| Notebook exploratório | ✅ |
| Workflow n8n | ✅ |
| Skill de IA | ✅ |
| Integração com OpenAI | Opcional |

---

# 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologias |
|------------|-------------|
| Linguagem | Python 3.12 |
| Manipulação de Dados | Pandas |
| Visualização | Matplotlib |
| Inteligência Artificial | OpenAI API *(opcional)* |
| Testes | Pytest |
| Notebook | Jupyter Notebook |
| Automação | n8n |
| Versionamento | Git e GitHub |

---

# 🔄 Fluxo do Pipeline

```text
                  World Bank Education Statistics
                               │
                               ▼
                    Carregamento dos Dados
                               │
                               ▼
                    Limpeza e Validação
                               │
                               ▼
              Transformação para Long Format
                               │
                               ▼
                Seleção de Indicadores
                               │
                               ▼
                 Cálculo das Métricas
                               │
                               ▼
               Rankings e Comparações
                               │
                               ▼
                 Geração de Gráficos
                               │
                               ▼
               Exportação dos Resultados
                               │
                               ▼
              Geração de Relatórios
                               │
                               ▼
         OpenAI (Análise Executiva Opcional)
```

---

# 📂 Estrutura do Projeto

```text
educacao-global-ai-agent/
│
├── data/
│   ├── raw/
│   │   ├── EdStatsCountry.csv
│   │   ├── EdStatsData.csv
│   │   ├── EdStatsFootNote.csv
│   │   └── EdStatsSeries.csv
│   │
│   ├── processed/
│   │   ├── education_clean.csv
│   │   └── education_filtered.csv
│   │
│   └── output/
│       ├── education_metrics.csv
│       ├── final_analysis.csv
│       ├── final_analysis.json
│       ├── rankings.csv
│       ├── country_comparison.csv
│       └── charts/
│           ├── historical_evolution.png
│           └── ranking_final_value.png
│
├── docs/
│   ├── architecture.md
│   ├── codex_usage.md
│   ├── data_dictionary.md
│   └── video_script.md
│
├── n8n/
│   ├── README-n8n.md
│   └── workflow.json
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── reports/
│   ├── report.md
│   ├── report.json
│   └── report.pdf
│
├── skills/
│   └── education-insight-skill/
│       ├── SKILL.md
│       ├── schema.json
│       ├── prompt_template.md
│       └── examples.md
│
├── src/
│   ├── __init__.py
│   ├── charts.py
│   ├── clean_data.py
│   ├── comparisons.py
│   ├── config.py
│   ├── exporters.py
│   ├── indicators.py
│   ├── load_data.py
│   ├── main.py
│   ├── metrics.py
│   ├── openai_client.py
│   ├── rankings.py
│   ├── report_generator.py
│   ├── transformations.py
│   └── utils.py
│
├── tests/
│   ├── test_clean_data.py
│   ├── test_comparisons.py
│   ├── test_indicators.py
│   ├── test_metrics.py
│   └── test_rankings.py
│
├── .env.example
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
└── requirements.txt
```

A estrutura foi organizada de forma modular para facilitar manutenção, escalabilidade e reutilização dos componentes, mantendo separadas as etapas de processamento, documentação, testes e artefatos gerados pelo pipeline.

---

# ⚙️ Instalação

## Pré-requisitos

Antes de executar o projeto, certifique-se de possuir:

- Python 3.12 ou superior;
- Git;
- Ambiente virtual (`venv`);
- Dataset **World Bank Education Statistics (EdStats)**.

---

## Clonando o repositório

```bash
git clone https://github.com/SEU-USUARIO/educacao-global-ai-agent.git

cd educacao-global-ai-agent
```

---

## Criando o ambiente virtual

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Instalando as dependências

```bash
pip install -r requirements.txt
```

---

# 📁 Estrutura esperada dos dados

Os arquivos do dataset devem ser colocados na pasta:

```text
data/raw/
```

Arquivos necessários:

```text
EdStatsCountry.csv
EdStatsData.csv
EdStatsFootNote.csv
EdStatsSeries.csv
```

---

# ▶️ Executando o Pipeline

## Execução padrão

```bash
python -m src.main --skip-openai
```

Durante a execução, o pipeline realiza automaticamente:

1. Carregamento dos dados;
2. Limpeza e validação;
3. Transformação para formato analítico;
4. Seleção dos indicadores;
5. Cálculo das métricas;
6. Geração dos rankings;
7. Comparação entre países;
8. Geração dos gráficos;
9. Exportação dos resultados;
10. Geração dos relatórios.

---

## Execução com OpenAI (Opcional)

Para habilitar a geração de análises executivas utilizando modelos da OpenAI, crie um arquivo `.env` na raiz do projeto contendo:

```env
OPENAI_API_KEY=sua_chave_da_api
OPENAI_MODEL=gpt-4.1-mini
```

Em seguida execute:

```bash
python -m src.main
```

> **Importante:** o projeto funciona normalmente sem a API da OpenAI. A integração é utilizada apenas para gerar análises executivas em linguagem natural.

---

# 📊 Resultados Gerados

Ao final da execução são produzidos automaticamente os seguintes arquivos.

## Dados processados

```text
data/output/

├── education_metrics.csv
├── rankings.csv
├── country_comparison.csv
├── final_analysis.csv
└── final_analysis.json
```

## Visualizações

```text
data/output/charts/

├── historical_evolution.png
└── ranking_final_value.png
```

## Relatórios

```text
reports/

├── report.md
├── report.json
└── report.pdf
```

---

# 🧪 Testes Automatizados

O projeto utiliza **Pytest** para validar os principais módulos do pipeline.

Para executar todos os testes:

```bash
pytest
```

Ou executar um teste específico:

```bash
pytest tests/test_metrics.py
```

Os testes contemplam funcionalidades como:

- limpeza dos dados;
- cálculo das métricas;
- rankings;
- comparação entre países;
- seleção de indicadores.

---

# 📚 Documentação

Além deste README, o projeto possui documentação complementar para facilitar a compreensão da arquitetura e da solução.

| Documento | Descrição |
|-----------|-----------|
| `docs/architecture.md` | Arquitetura da solução e organização dos componentes |
| `docs/data_dictionary.md` | Descrição do dataset e principais campos utilizados |
| `docs/codex_usage.md` | Histórico de desenvolvimento e uso de IA durante o projeto |
| `docs/video_script.md` | Roteiro da apresentação em vídeo |

---

# 🎁 Funcionalidades Extras

Além dos requisitos principais do desafio, foram implementados recursos adicionais para tornar a solução mais completa e preparada para futuras evoluções.

## 🧠 Skill de IA

A pasta `skills/education-insight-skill/` contém uma Skill estruturada para reutilização em aplicações baseadas em Modelos de Linguagem (LLMs).

Arquivos incluídos:

- `SKILL.md`
- `schema.json`
- `prompt_template.md`
- `examples.md`

---

## 🔄 Workflow n8n

Foi incluído um workflow de exemplo utilizando **n8n**, demonstrando como o pipeline pode ser integrado a processos automatizados.

Arquivos disponíveis:

```text
n8n/
├── README-n8n.md
└── workflow.json
```

---

## 📓 Notebook Exploratório

O projeto também inclui um notebook Jupyter com uma análise exploratória do dataset.

```text
notebooks/
└── exploratory_analysis.ipynb
```

Esse material pode ser utilizado para exploração dos dados, testes e futuras análises.

---

# 📈 Possíveis Evoluções

A arquitetura foi desenvolvida para facilitar novas funcionalidades, como:

- integração com novos indicadores educacionais;
- comparação entre regiões e continentes;
- criação de dashboards interativos;
- integração com APIs do World Bank;
- automação completa utilizando n8n;
- suporte a novos modelos de IA.

---

# 🤖 Desenvolvimento Assistido por IA

Durante o desenvolvimento deste projeto foram utilizadas técnicas de Engenharia de Prompt para apoiar as etapas de análise, planejamento, implementação e revisão da solução.

Os principais frameworks e estratégias empregados incluíram:

- Quebrador de Problemas (decomposição do desafio em módulos menores);
- Arquiteto de Soluções de IA (definição da arquitetura do sistema);
- Gerador de Prompts (estruturação de prompts especializados);
- Desenvolvimento incremental orientado por IA;
- Revisão iterativa de código e documentação.

A Inteligência Artificial foi utilizada como ferramenta de apoio ao desenvolvimento, enquanto todas as decisões de arquitetura, validação, testes e integração dos componentes foram conduzidas durante a implementação do projeto.

---


# 📄 Licença

Este projeto está licenciado sob a **Licença MIT**.

Consulte o arquivo **LICENSE** para mais informações.

---

# 👩‍💻 Autora

**Bárbara Castro**

Projeto desenvolvido como parte do desafio **Agente de Inteligência Global em Educação**, utilizando o dataset **World Bank Education Statistics (EdStats)**.

---

# 🙏 Agradecimentos

Agradecimentos à organização do desafio pela proposta prática, que possibilitou o desenvolvimento de uma solução completa envolvendo processamento de dados, arquitetura de software, Inteligência Artificial e automação.

Também agradeço ao **World Bank** pela disponibilização do dataset **Education Statistics (EdStats)**, utilizado como base para todas as análises realizadas neste projeto.

