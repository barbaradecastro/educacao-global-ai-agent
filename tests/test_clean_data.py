import pandas as pd
import pytest

from src.clean_data import clean_education_data


def _sample_raw_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Country Name": [" Brazil ", "Chile", None],
            "Country Code": [" bra ", "chl", "ARG"],
            "Indicator Name": [" Literacy Rate ", "Education Spending", "Literacy Rate"],
            "Indicator Code": [" se.adt.litr.zs ", "se.xpd.totl.gd.zs", "se.adt.litr.zs"],
            "2000": ["90.5", "4.2", "95.1"],
            "2020": ["95.0", "5.1", None],
            "Empty Column": [None, None, None],
        }
    )


def test_clean_education_data_removes_empty_columns():
    result = clean_education_data(
        _sample_raw_dataframe(),
        save_output=False,
    )

    assert "Empty Column" not in result.columns


def test_clean_education_data_standardizes_text_columns():
    result = clean_education_data(
        _sample_raw_dataframe(),
        save_output=False,
    )

    assert result.iloc[0]["Country Name"] == "Brazil"
    assert result.iloc[0]["Country Code"] == "BRA"
    assert result.iloc[0]["Indicator Name"] == "Literacy Rate"
    assert result.iloc[0]["Indicator Code"] == "SE.ADT.LITR.ZS"


def test_clean_education_data_converts_year_columns_to_numeric():
    result = clean_education_data(
        _sample_raw_dataframe(),
        save_output=False,
    )

    assert pd.api.types.is_numeric_dtype(result["2000"])
    assert pd.api.types.is_numeric_dtype(result["2020"])


def test_clean_education_data_removes_rows_missing_required_fields():
    result = clean_education_data(
        _sample_raw_dataframe(),
        save_output=False,
    )

    assert len(result) == 2


def test_clean_education_data_rejects_invalid_input():
    with pytest.raises(TypeError):
        clean_education_data(
            "invalid input",
            save_output=False,
        )