# Project Usage Guide

## Overview

The Global Education AI Agent is a modular Python application that analyzes educational indicators from the World Bank Education Statistics (EdStats) dataset.

The pipeline performs:

- Data loading
- Data cleaning
- Data transformation
- Indicator filtering
- Metrics calculation
- Country rankings
- Country comparison
- Chart generation
- Executive report generation
- Export of analytical artifacts

---

# Requirements

- Python 3.12 or higher
- Git
- Virtual Environment (venv)

---

# Installation

Clone the repository:

```bash
git clone https://github.com/<your-user>/educacao-global-ai-agent.git
```

Enter the project folder:

```bash
cd educacao-global-ai-agent
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Dataset

Download the official World Bank Education Statistics dataset.

Required files:

```
EdStatsData.csv
EdStatsCountry.csv
EdStatsSeries.csv
EdStatsFootNote.csv
```

Copy all files to:

```
data/raw/
```

---

# Environment Variables

Create a file named:

```
.env
```

Example:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
```

If you do not intend to use OpenAI, the API key is not required.

---

# Running the Pipeline

## Full execution

```bash
python -m src.main
```

This command executes:

- data loading
- cleaning
- transformation
- metrics
- rankings
- comparisons
- charts
- exports
- OpenAI executive analysis

---

## Execution without OpenAI

```bash
python -m src.main --skip-openai
```

Recommended when:

- no OpenAI API key is available
- offline execution
- testing the analytical pipeline

---

# Default Parameters

Countries:

```
BRA
CHL
ARG
USA
FIN
```

Indicators:

```
SE.XPD.TOTL.GD.ZS
SE.ADT.LITR.ZS
```

Period:

```
2000–2020
```

---

# Custom Parameters

Example:

```bash
python -m src.main \
    --countries BRA USA CAN \
    --indicators SE.ADT.LITR.ZS \
    --start-year 1995 \
    --end-year 2022
```

---

# Generated Outputs

CSV

```
education_metrics.csv
rankings.csv
country_comparison.csv
final_analysis.csv
```

JSON

```
report.json
final_analysis.json
```

Markdown

```
report.md
```

Charts

```
ranking_final_value.png

historical_evolution.png
```

---

# Project Structure

```
src/
data/
reports/
docs/
skills/
n8n/
tests/
```

---

# Logging

All modules use the Python logging package.

Typical execution log:

```
Loading data...

Cleaning dataset...

Calculating metrics...

Generating charts...

Exporting reports...

Pipeline completed successfully.
```

---

# Error Handling

The project validates:

- missing files
- invalid country codes
- invalid indicators
- invalid years
- missing required columns
- invalid DataFrames
- export errors
- OpenAI configuration

All exceptions are logged before being propagated.

---

# OpenAI Integration

The OpenAI integration is optional.

When enabled, the project sends a structured analytical payload to generate an executive educational report.

If the API key is unavailable, execute:

```bash
python -m src.main --skip-openai
```

---

# Development Notes

The project follows:

- modular architecture
- separation of concerns
- reusable components
- extensive logging
- type hints
- Google-style docstrings
- defensive validation
- structured exception handling

---

# Future Improvements

Potential enhancements include:

- Interactive dashboard
- Streamlit interface
- FastAPI REST API
- Automated n8n workflow
- Scheduled execution
- Docker support
- Cloud deployment
- Additional educational indicators
- Automated unit tests