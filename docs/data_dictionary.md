# Data Dictionary

## Overview

This project uses the **World Bank Education Statistics (EdStats)** dataset, one of the largest public educational databases available worldwide.

The dataset contains thousands of educational indicators collected for more than 200 countries over several decades.

Official source:

- World Bank Education Statistics (EdStats)
- https://datacatalog.worldbank.org/search/dataset/0038480/education-statistics

---

# Main Dataset

File:

```
EdStatsData.csv
```

Contains the historical values for all educational indicators.

Each row represents:

```
Country
+
Educational Indicator
+
Historical values (one column per year)
```

---

# Main Columns

| Column | Description |
|---------|-------------|
| Country Name | Country name |
| Country Code | ISO 3-letter country code |
| Indicator Name | Educational indicator description |
| Indicator Code | World Bank indicator code |
| 1970 ... 2024 | Historical values by year |

---

# Country Dataset

File:

```
EdStatsCountry.csv
```

Contains metadata about countries.

Examples:

- Region
- Income Group
- Lending Category
- Special Notes

---

# Indicator Dataset

File:

```
EdStatsSeries.csv
```

Contains metadata describing each educational indicator.

Examples:

- Indicator name
- Indicator code
- Long definition
- Statistical methodology
- Source notes

---

# Footnote Dataset

File:

```
EdStatsFootNote.csv
```

Contains explanatory notes regarding specific observations.

Examples:

- Missing values
- Estimation notes
- Methodological remarks

---

# Analytical Dataset

After processing, the project transforms the original dataset into a normalized long format.

Generated columns:

| Column | Description |
|---------|-------------|
| country | Country name |
| country_code | ISO code |
| indicator_code | Indicator identifier |
| indicator_name | Indicator description |
| year | Observation year |
| value | Indicator value |

---

# Metrics Dataset

The project generates an analytical dataset containing summarized metrics.

Columns include:

| Column | Description |
|---------|-------------|
| start_year | First available year |
| end_year | Last available year |
| initial_value | Initial observed value |
| final_value | Final observed value |
| historical_mean | Mean historical value |
| absolute_growth | Difference between final and initial values |
| percentage_growth | Relative percentage growth |
| valid_observations | Number of valid observations |
| trend | Growth classification |

---

# Supported Indicators

The pipeline supports any indicator available in the EdStats dataset.

Example indicators:

| Indicator Code | Description |
|----------------|-------------|
| SE.XPD.TOTL.GD.ZS | Government expenditure on education (% of GDP) |
| SE.ADT.LITR.ZS | Adult literacy rate (%) |

Additional indicators can be analyzed simply by informing their official World Bank code.

---

# Countries

The application accepts any ISO 3166-1 alpha-3 country code available in the dataset.

Examples:

| Code | Country |
|------|----------|
| BRA | Brazil |
| ARG | Argentina |
| CHL | Chile |
| USA | United States |
| FIN | Finland |

---

# Data Processing Workflow

```
Raw CSV
      ↓
Validation
      ↓
Cleaning
      ↓
Transformation
      ↓
Indicator Filtering
      ↓
Metric Calculation
      ↓
Ranking
      ↓
Comparison
      ↓
Visualization
      ↓
Executive Report
```

---

# Output Files

The project generates:

- education_clean.csv
- education_metrics.csv
- rankings.csv
- country_comparison.csv
- final_analysis.csv
- final_analysis.json
- report.md
- report.json
- ranking_final_value.png
- historical_evolution.png

---

# Data Quality

Before analysis, the pipeline performs several validation and cleaning steps:

- Validation of required columns
- Removal of empty columns
- Removal of invalid records
- Numeric conversion of year columns
- Standardization of text fields
- Validation of country codes
- Validation of indicator codes
- Validation of year ranges

These steps ensure consistency and reliability throughout the analytical pipeline.