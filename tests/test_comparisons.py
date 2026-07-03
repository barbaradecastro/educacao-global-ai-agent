import pandas as pd
import pytest

from src.comparisons import compare_countries


def _sample_metrics_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "country": [
                "Brazil",
                "Chile",
                "Finland",
                "Argentina",
            ],
            "country_code": [
                "BRA",
                "CHL",
                "FIN",
                "ARG",
            ],
            "indicator_code": [
                "TEST.IND",
                "TEST.IND",
                "TEST.IND",
                "TEST.IND",
            ],
            "indicator_name": [
                "Test Indicator",
                "Test Indicator",
                "Test Indicator",
                "Test Indicator",
            ],
            "start_year": [2000, 2000, 2000, 2000],
            "end_year": [2020, 2020, 2020, 2020],
            "initial_value": [40, 50, 60, 55],
            "final_value": [60, 80, 90, 70],
            "historical_mean": [50, 65, 75, 62],
            "absolute_growth": [20, 30, 30, 15],
            "percentage_growth": [50, 60, 50, 27.3],
            "valid_observations": [21, 21, 21, 21],
            "trend": [
                "crescimento",
                "crescimento",
                "crescimento",
                "crescimento",
            ],
        }
    )


def test_compare_selected_countries():
    result = compare_countries(
        _sample_metrics_df(),
        countries=["BRA", "FIN"],
    )

    assert len(result) == 2
    assert set(result["country_code"]) == {"BRA", "FIN"}


def test_compare_selected_indicator():
    result = compare_countries(
        _sample_metrics_df(),
        countries=["BRA", "CHL"],
        indicator_code="TEST.IND",
    )

    assert len(result) == 2
    assert all(result["indicator_code"] == "TEST.IND")


def test_compare_returns_expected_columns():
    result = compare_countries(
        _sample_metrics_df(),
        countries=["BRA", "CHL"],
    )

    expected_columns = {
        "country",
        "country_code",
        "indicator_code",
        "final_value",
    }

    assert expected_columns.issubset(result.columns)


def test_compare_invalid_dataframe():
    with pytest.raises(TypeError):
        compare_countries(
            [],
            countries=["BRA"],
        )