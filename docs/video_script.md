# Roteiro da Apresentação do Vídeo — Global Education AI Agent

Tempo estimado: 5 a 6 minutos

---

# 1. Apresentação (30 segundos)

Olá!

Meu nome é Bárbara Castro e este é o projeto **Global Education AI Agent**, desenvolvido como solução para o desafio proposto.

O objetivo do projeto é automatizar a análise de indicadores educacionais do World Bank Education Statistics (EdStats), utilizando Python, Inteligência Artificial e uma arquitetura modular capaz de processar grandes volumes de dados de forma automatizada.

---

# 2. Visão Geral do Projeto (40 segundos)

A solução foi desenvolvida utilizando uma arquitetura modular.

Cada responsabilidade foi separada em um módulo específico, tornando o projeto organizado, reutilizável e de fácil manutenção.

Os principais módulos são:

- carregamento dos dados;
- limpeza;
- transformação;
- cálculo de métricas;
- rankings;
- comparações entre países;
- geração de gráficos;
- exportação dos resultados;
- geração de relatórios;
- integração opcional com a OpenAI.

Além disso, o projeto possui documentação, testes automatizados e materiais extras para expansão futura.

---

# 3. Estrutura do Projeto (40 segundos)

Agora vou apresentar rapidamente a estrutura do projeto.

Na pasta **src** estão todos os módulos responsáveis pelo pipeline.

Na pasta **data** ficam os arquivos de entrada e os resultados gerados.

A pasta **reports** contém os relatórios produzidos automaticamente.

Também foram incluídas as pastas:

- docs
- tests
- skills
- n8n
- notebooks

que complementam a solução proposta.

---

# 4. Execução do Pipeline (1 minuto e 30 segundos)

Agora vou executar o pipeline principal.

No terminal utilizo o comando:

python -m src.main --skip-openai

Durante a execução é possível acompanhar todas as etapas através dos logs.

O sistema realiza automaticamente:

• carregamento do dataset;

• limpeza dos dados;

• transformação para formato analítico;

• seleção dos indicadores;

• cálculo das métricas;

• geração dos rankings;

• comparação entre países;

• geração de gráficos;

• exportação dos resultados;

• criação dos relatórios em Markdown e JSON.

Todo esse processo ocorre automaticamente.

---

# 5. Resultados (1 minuto)

Após a execução, os resultados são gravados automaticamente.

Na pasta **data/output** encontramos arquivos como:

- education_metrics.csv
- rankings.csv
- country_comparison.csv
- final_analysis.csv
- final_analysis.json

Também são gerados gráficos automaticamente.

Na pasta **reports** são produzidos relatórios estruturados que resumem toda a análise realizada pelo pipeline.

---

# 6. Testes Automatizados (40 segundos)

O projeto também possui testes automatizados utilizando Pytest.

Esses testes validam módulos importantes como:

- limpeza dos dados;
- cálculo das métricas;
- rankings;
- comparações;
- indicadores.

Os testes ajudam a garantir que futuras alterações não comprometam o funcionamento da aplicação.

---

# 7. Diferenciais (50 segundos)

Além da implementação principal, foram desenvolvidos alguns diferenciais para tornar a solução mais completa.

Entre eles:

• documentação técnica;

• notebook de análise exploratória;

• Skill de IA preparada para integração futura;

• workflow do n8n;

• arquitetura modular;

• geração automática de relatórios;

• integração opcional com modelos da OpenAI.

Esses componentes tornam o projeto escalável e preparado para futuras evoluções.

---

# 8. Encerramento (30 segundos)

Este projeto demonstra como Inteligência Artificial, análise de dados e engenharia de software podem ser combinadas para automatizar a geração de informações estratégicas sobre indicadores educacionais.

Muito obrigada pela oportunidade de apresentar esta solução.

Espero que o projeto demonstre não apenas o funcionamento da aplicação, mas também a preocupação com organização, documentação, qualidade do código e escalabilidade.

Obrigado!