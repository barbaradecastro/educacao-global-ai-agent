import pandas as pd
import pytest

from src.indicators import (
    filter_indicators,
    list_available_indicators,
    map_indicator_names,
    validate_selected_indicators,
)


def _sample_indicators_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "country": ["Brazil", "Brazil", "Chile"],
            "country_code": ["BRA", "BRA", "CHL"],
            "indicator_code": ["IND.A", "IND.B", "IND.A"],
            "indicator_name": ["Indicator A", "Indicator B", "Indicator A"],
            "year": [2020, 2020, 2020],
            "value": [10, 20, 30],
        }
    )


def test_list_available_indicators():
    result = list_available_indicators(_sample_indicators_df())

    assert len(result) == 2
    assert set(result["indicator_code"]) == {"IND.A", "IND.B"}


def test_validate_selected_indicators_success():
    validate_selected_indicators(
        _sample_indicators_df(),
        ["IND.A", "IND.B"],
    )


def test_validate_selected_indicators_invalid():
    with pytest.raises(ValueError):
        validate_selected_indicators(
            _sample_indicators_df(),
            ["IND.X"],
        )


def test_map_indicator_names():
    result = map_indicator_names(_sample_indicators_df())

    assert result["IND.A"] == "Indicator A"
    assert result["IND.B"] == "Indicator B"


def test_filter_indicators():
    result = filter_indicators(
        _sample_indicators_df(),
        ["IND.A"],
    )

    assert len(result) == 2
    assert set(result["indicator_code"]) == {"IND.A"}