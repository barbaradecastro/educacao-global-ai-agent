# Architecture

## Overview

The Global Education AI Agent is a modular data analytics pipeline built in Python for processing the World Bank Education Statistics (EdStats) dataset.

The application automates the complete analytical workflow, from loading raw educational data to generating executive reports enriched by Artificial Intelligence.

The architecture follows a layered and modular design, making each component responsible for a single stage of the pipeline.

---

# High-Level Architecture

```
                 +----------------------+
                 | World Bank EdStats   |
                 | CSV Dataset          |
                 +----------+-----------+
                            |
                            v
                  load_data.py
                            |
                            v
                  clean_data.py
                            |
                            v
              transformations.py
                            |
                            v
                 indicators.py
                            |
                            v
                  metrics.py
                            |
                +-----------+------------+
                |                        |
                v                        v
         rankings.py             comparisons.py
                |                        |
                +-----------+------------+
                            |
                            v
                     charts.py
                            |
                            v
                 report_generator.py
                            |
                            +------------------+
                            |                  |
                            v                  v
                 exporters.py          openai_client.py
                            |
                            v
                  Markdown / JSON / CSV
```

---

# Project Layers

## Data Layer

Responsible for reading the raw World Bank datasets.

Module:

- load_data.py

Input:

- EdStatsData.csv
- EdStatsCountry.csv
- EdStatsSeries.csv
- EdStatsFootNote.csv

Output:

- Raw pandas DataFrames

---

## Data Preparation Layer

Responsible for:

- Removing invalid records
- Converting numeric values
- Cleaning missing values
- Standardizing columns

Module:

- clean_data.py

---

## Transformation Layer

Converts the original wide dataset into long format.

Module:

- transformations.py

Main operation:

- pandas.melt()

---

## Indicator Layer

Filters only the indicators selected by the user.

Module:

- indicators.py

Example indicators:

- SE.XPD.TOTL.GD.ZS
- SE.ADT.LITR.ZS

---

## Analytics Layer

Calculates analytical metrics for each country and indicator.

Module:

- metrics.py

Generated metrics include:

- Initial value
- Final value
- Absolute growth
- Percentage growth
- CAGR
- Trend classification

---

## Ranking Layer

Ranks countries based on analytical metrics.

Module:

- rankings.py

---

## Comparison Layer

Compares selected countries using a common indicator.

Module:

- comparisons.py

---

## Visualization Layer

Generates analytical charts.

Module:

- charts.py

Charts:

- Ranking Bar Chart
- Historical Time Series

---

## AI Layer

Responsible for generating executive reports using OpenAI.

Module:

- openai_client.py

This layer is optional and can be skipped using:

```

--skip-openai

```

---

## Reporting Layer

Builds structured reports.

Module:

- report_generator.py

Generated formats:

- Markdown
- JSON

---

## Export Layer

Exports all generated artifacts.

Module:

- exporters.py

Supported formats:

- CSV
- JSON
- Markdown

---

# Main Execution Flow

```
Load Dataset
      ↓
Clean Data
      ↓
Transform Data
      ↓
Filter Indicators
      ↓
Calculate Metrics
      ↓
Generate Rankings
      ↓
Compare Countries
      ↓
Create Charts
      ↓
Generate AI Report (optional)
      ↓
Export Results
```

---

# Technologies

- Python 3.12
- Pandas
- Matplotlib
- OpenAI API
- argparse
- JSON
- CSV

---

# Design Principles

The project follows the following software engineering principles:

- Modular Architecture
- Single Responsibility Principle (SRP)
- Separation of Concerns
- Reusable Components
- Explicit Type Hints
- Comprehensive Logging
- Exception Handling
- Configurable Pipeline