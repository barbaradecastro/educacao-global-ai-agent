import pandas as pd
import pytest

from src.rankings import (
    get_bottom_n,
    get_top_n,
    rank_by_absolute_growth,
    rank_by_final_value,
    rank_by_percentage_growth,
)


def _sample_metrics_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "country": ["Brazil", "Chile", "Finland"],
            "country_code": ["BRA", "CHL", "FIN"],
            "indicator_code": ["TEST.IND", "TEST.IND", "TEST.IND"],
            "indicator_name": ["Test Indicator", "Test Indicator", "Test Indicator"],
            "final_value": [70, 90, 80],
            "absolute_growth": [10, 30, 20],
            "percentage_growth": [16.6, 50.0, 33.3],
        }
    )


def test_rank_by_final_value_orders_descending():
    result = rank_by_final_value(_sample_metrics_df())

    assert result.iloc[0]["country_code"] == "CHL"
    assert result.iloc[1]["country_code"] == "FIN"
    assert result.iloc[2]["country_code"] == "BRA"
    assert list(result["rank"]) == [1, 2, 3]


def test_rank_by_absolute_growth_orders_descending():
    result = rank_by_absolute_growth(_sample_metrics_df())

    assert result.iloc[0]["country_code"] == "CHL"
    assert result.iloc[1]["country_code"] == "FIN"
    assert result.iloc[2]["country_code"] == "BRA"


def test_rank_by_percentage_growth_orders_descending():
    result = rank_by_percentage_growth(_sample_metrics_df())

    assert result.iloc[0]["country_code"] == "CHL"
    assert result.iloc[1]["country_code"] == "FIN"
    assert result.iloc[2]["country_code"] == "BRA"


def test_get_top_n_returns_expected_number_of_rows():
    result = get_top_n(_sample_metrics_df(), n=2)

    assert len(result) == 2
    assert result.iloc[0]["country_code"] == "CHL"


def test_get_bottom_n_returns_expected_number_of_rows():
    result = get_bottom_n(_sample_metrics_df(), n=2)

    assert len(result) == 2
    assert result.iloc[0]["country_code"] == "BRA"


def test_invalid_metric_raises_value_error():
    with pytest.raises(ValueError):
        get_top_n(_sample_metrics_df(), metric="invalid_metric", n=2)