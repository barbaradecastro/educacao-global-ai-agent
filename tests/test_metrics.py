import pandas as pd

from src.metrics import calculate_metrics


def test_calculate_metrics_returns_expected_columns():
    df = pd.DataFrame(
        {
            "country": ["Brazil", "Brazil", "Brazil"],
            "country_code": ["BRA", "BRA", "BRA"],
            "indicator_code": ["TEST.IND", "TEST.IND", "TEST.IND"],
            "indicator_name": ["Test Indicator", "Test Indicator", "Test Indicator"],
            "year": [2000, 2010, 2020],
            "value": [10, 15, 20],
        }
    )

    result = calculate_metrics(df)

    expected_columns = [
        "country",
        "country_code",
        "indicator_code",
        "indicator_name",
        "start_year",
        "end_year",
        "initial_value",
        "final_value",
        "historical_mean",
        "absolute_growth",
        "percentage_growth",
        "valid_observations",
        "trend",
    ]

    assert list(result.columns) == expected_columns


def test_calculate_metrics_growth_values():
    df = pd.DataFrame(
        {
            "country": ["Brazil", "Brazil"],
            "country_code": ["BRA", "BRA"],
            "indicator_code": ["TEST.IND", "TEST.IND"],
            "indicator_name": ["Test Indicator", "Test Indicator"],
            "year": [2000, 2020],
            "value": [10, 20],
        }
    )

    result = calculate_metrics(df)
    row = result.iloc[0]

    assert row["start_year"] == 2000
    assert row["end_year"] == 2020
    assert row["initial_value"] == 10
    assert row["final_value"] == 20
    assert row["absolute_growth"] == 10
    assert row["percentage_growth"] == 100
    assert row["trend"] == "crescimento"


def test_calculate_metrics_classifies_stability():
    df = pd.DataFrame(
        {
            "country": ["Brazil", "Brazil"],
            "country_code": ["BRA", "BRA"],
            "indicator_code": ["TEST.IND", "TEST.IND"],
            "indicator_name": ["Test Indicator", "Test Indicator"],
            "year": [2000, 2020],
            "value": [100, 103],
        }
    )

    result = calculate_metrics(df)

    assert result.iloc[0]["trend"] == "estabilidade"


def test_calculate_metrics_handles_zero_initial_value():
    df = pd.DataFrame(
        {
            "country": ["Brazil", "Brazil"],
            "country_code": ["BRA", "BRA"],
            "indicator_code": ["TEST.IND", "TEST.IND"],
            "indicator_name": ["Test Indicator", "Test Indicator"],
            "year": [2000, 2020],
            "value": [0, 20],
        }
    )

    result = calculate_metrics(df)

    assert pd.isna(result.iloc[0]["percentage_growth"])
    assert result.iloc[0]["trend"] == "indefinido"