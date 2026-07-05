# Roteiro da Apresentação do Vídeo — Global Education AI Agent (5–10 minutos) 

# 1. Apresentação

Olá!

Meu nome é **Bárbara Castro** e este é o projeto **Global Education AI Agent**, desenvolvido para o desafio **Acelera AI**.

O objetivo da solução é automatizar o processamento e a análise de indicadores educacionais utilizando dados do **World Bank Education Statistics (EdStats)**, integrando Python, OpenAI, n8n e Skills.

---

# 2. Objetivo do Projeto

O pipeline foi desenvolvido para:

- processar dados educacionais;
- selecionar países e indicadores;
- comparar resultados entre países;
- gerar rankings;
- produzir gráficos;
- gerar relatórios automatizados;
- produzir análises executivas utilizando Inteligência Artificial.

---

# 3. Arquitetura

Apresente rapidamente a estrutura do projeto:

- `src/`
- `tests/`
- `docs/`
- `skills/`
- `n8n/`
- `reports/`
- `notebooks/`

Explique que a arquitetura foi organizada de forma modular para facilitar manutenção, reutilização e evolução da solução.

---

# 4. Execução do Pipeline

Execute:

```bash
python -m src.main --skip-openai
```

Durante a execução, explique que o pipeline realiza automaticamente:

- carregamento dos dados;
- limpeza;
- transformação;
- seleção de indicadores;
- cálculo das métricas;
- geração dos rankings;
- comparação entre países;
- geração dos gráficos;
- exportação dos resultados;
- geração dos relatórios.

---

# 5. Resultados

Mostre:

- gráficos gerados;
- arquivos CSV;
- arquivos JSON;
- relatório Markdown;
- notebook exploratório.

Comente rapidamente alguns resultados observados, como diferenças entre países, rankings e tendências identificadas pelo pipeline.

---

# 6. OpenAI

Explique que a integração com a OpenAI é opcional.

Quando configurada a chave da API, o sistema produz automaticamente uma análise executiva baseada nos indicadores processados, incluindo:

- principais resultados;
- evolução dos países;
- tendências;
- recomendações;
- limitações da análise.

---

# 7. Workflow n8n

Apresente o arquivo `workflow.json`.

Explique que o workflow automatiza o processo utilizando:

- gatilho periódico;
- execução do pipeline Python;
- leitura dos resultados;
- chamada para a OpenAI;
- armazenamento do relatório final.

---

# 8. Skill

Apresente rapidamente a pasta `skills/education-insight-skill`.

Explique que a Skill foi desenvolvida para reutilizar capacidades de análise educacional em aplicações baseadas em Modelos de Linguagem (LLMs).

Mostre os arquivos:

- `SKILL.md`
- `schema.json`
- `prompt_template.md`
- `examples.md`

---

# 9. Como o Codex foi utilizado

Explique que o desenvolvimento contou com apoio do Codex em atividades como:

- implementação de funções Python;
- revisão de código;
- criação de testes automatizados;
- documentação técnica;
- organização da arquitetura;
- estruturação da Skill;
- documentação do workflow do n8n.

Ressalte que as decisões de arquitetura, integração dos módulos, validação dos resultados e organização final da solução foram conduzidas durante o desenvolvimento do projeto.

---

# 10. Encerramento

Finalize agradecendo pela oportunidade de participar do desafio.

Reforce que o projeto demonstra a integração entre:

- Python;
- OpenAI;
- n8n;
- Skills;
- desenvolvimento assistido por IA.

Agradeça pela atenção.