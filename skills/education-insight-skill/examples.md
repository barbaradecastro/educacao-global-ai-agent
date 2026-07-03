# Education Insight Skill — Usage Examples

This document presents practical examples of how the Education Insight Skill can be used after the project pipeline has processed the World Bank Education Statistics (EdStats) dataset.

---

# Example 1 — Country Comparison

## User Request

Compare Brazil and Finland regarding literacy rates between 2000 and 2020.

## Expected Response

- Present the historical evolution of both countries.
- Compare the final indicator values.
- Identify which country achieved the best result.
- Summarize the main differences.

---

# Example 2 — Ranking Analysis

## User Request

Show the top 10 countries with the highest education expenditure.

## Expected Response

- Display the ranking.
- Explain the ranking criterion.
- Highlight relevant differences among the leading countries.
- Mention possible data limitations.

---

# Example 3 — Historical Trend

## User Request

Analyze the evolution of education expenditure in Chile from 2000 to 2020.

## Expected Response

- Describe the historical behavior of the indicator.
- Report whether the trend indicates growth, stability or decline.
- Summarize the most significant changes observed.

---

# Example 4 — Executive Summary

## User Request

Generate an executive report for the selected countries.

## Expected Response

The report should include:

- Executive Summary
- Main Findings
- Country Comparison
- Rankings
- Historical Trends
- Educational Insights
- Conclusions

---

# Example 5 — Multiple Indicators

## User Request

Compare Brazil, Chile and Argentina using:

- Literacy Rate
- Education Expenditure

## Expected Response

The assistant should:

- Analyze each indicator independently.
- Compare the countries.
- Highlight similarities and differences.
- Produce a concise executive summary.

---

# Expected Behavior

The Skill should always:

- Use only the processed EdStats data.
- Base conclusions on the available evidence.
- Avoid unsupported assumptions.
- Clearly state when information is insufficient.
- Produce structured and objective responses.

---

# Integration

This Skill is designed to work together with the following project modules:

- load_data.py
- clean_data.py
- transformations.py
- indicators.py
- metrics.py
- rankings.py
- comparisons.py
- report_generator.py
- openai_client.py

The examples above assume that the analytical pipeline has already been executed successfully.