import pandas as pd

from .utils import setup_logger, validate_countries


logger = setup_logger(__name__)

COUNTRY_COLUMN = "country"
COUNTRY_CODE_COLUMN = "country_code"
INDICATOR_CODE_COLUMN = "indicator_code"
INDICATOR_NAME_COLUMN = "indicator_name"
FINAL_VALUE_COLUMN = "final_value"
HISTORICAL_MEAN_COLUMN = "historical_mean"
ABSOLUTE_GROWTH_COLUMN = "absolute_growth"
PERCENTAGE_GROWTH_COLUMN = "percentage_growth"
TREND_COLUMN = "trend"

LEADER_COUNTRY_COLUMN = "leader_country"
LEADER_COUNTRY_CODE_COLUMN = "leader_country_code"
LEADER_VALUE_COLUMN = "leader_value"
LOWEST_COUNTRY_COLUMN = "lowest_country"
LOWEST_COUNTRY_CODE_COLUMN = "lowest_country_code"
LOWEST_VALUE_COLUMN = "lowest_value"
DIFFERENCE_TO_LEADER_COLUMN = "difference_to_leader"
PERCENTAGE_DIFFERENCE_TO_LEADER_COLUMN = "percentage_difference_to_leader"

REQUIRED_COLUMNS: list[str] = [
    COUNTRY_COLUMN,
    COUNTRY_CODE_COLUMN,
    INDICATOR_CODE_COLUMN,
    INDICATOR_NAME_COLUMN,
    FINAL_VALUE_COLUMN,
    HISTORICAL_MEAN_COLUMN,
    ABSOLUTE_GROWTH_COLUMN,
    PERCENTAGE_GROWTH_COLUMN,
    TREND_COLUMN,
]

FINAL_COLUMNS: list[str] = [
    COUNTRY_COLUMN,
    COUNTRY_CODE_COLUMN,
    INDICATOR_CODE_COLUMN,
    INDICATOR_NAME_COLUMN,
    FINAL_VALUE_COLUMN,
    HISTORICAL_MEAN_COLUMN,
    ABSOLUTE_GROWTH_COLUMN,
    PERCENTAGE_GROWTH_COLUMN,
    TREND_COLUMN,
    LEADER_COUNTRY_COLUMN,
    LEADER_COUNTRY_CODE_COLUMN,
    LEADER_VALUE_COLUMN,
    LOWEST_COUNTRY_COLUMN,
    LOWEST_COUNTRY_CODE_COLUMN,
    LOWEST_VALUE_COLUMN,
    DIFFERENCE_TO_LEADER_COLUMN,
    PERCENTAGE_DIFFERENCE_TO_LEADER_COLUMN,
]


def _validate_dataframe(df: pd.DataFrame) -> None:
    """
    Validate that the input is a pandas DataFrame.

    Args:
        df: Object to validate.

    Raises:
        TypeError: If df is not a pandas DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")


def _validate_required_columns(df: pd.DataFrame) -> None:
    """
    Validate that required comparison columns exist in the DataFrame.

    Args:
        df: DataFrame to validate.

    Raises:
        KeyError: If one or more required columns are missing.
    """
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")


def _normalize_codes(codes: list[str]) -> list[str]:
    """
    Normalize a list of codes by removing spaces and converting to uppercase.

    Args:
        codes: List of country or indicator codes.

    Returns:
        Normalized list of codes.
    """
    return [code.strip().upper() for code in codes]


def _normalize_code(code: str, field_name: str) -> str:
    """
    Normalize a single code by removing spaces and converting to uppercase.

    Args:
        code: Code to normalize.
        field_name: Field name used in error messages.

    Returns:
        Normalized code.

    Raises:
        TypeError: If code is not a string.
        ValueError: If code is empty.
    """
    if not isinstance(code, str):
        raise TypeError(f"{field_name} must be a string.")

    normalized_code = code.strip().upper()

    if not normalized_code:
        raise ValueError(f"{field_name} must be a non-empty string.")

    return normalized_code


def filter_countries(
    df: pd.DataFrame,
    countries: list[str],
) -> pd.DataFrame:
    """
    Filter a metrics DataFrame by selected country codes.

    Args:
        df: Metrics DataFrame.
        countries: List of three-character country codes.

    Returns:
        Filtered DataFrame containing only selected countries.

    Raises:
        TypeError: If df or countries have invalid types.
        KeyError: If required columns are missing.
        ValueError: If no selected countries are found.
        Exception: For unexpected errors.
    """
    logger.info("Filtering DataFrame by countries.")

    try:
        _validate_dataframe(df)
        _validate_required_columns(df)
        validate_countries(countries)

        normalized_countries = _normalize_codes(countries)

        filtered_df = df[
            df[COUNTRY_CODE_COLUMN]
            .astype(str)
            .str.strip()
            .str.upper()
            .isin(normalized_countries)
        ].copy()

        filtered_df = filtered_df.reset_index(drop=True)

        if filtered_df.empty:
            raise ValueError(f"No records found for countries: {normalized_countries}")

        logger.info(
            "Filtered countries %s. Rows after filter: %s",
            normalized_countries,
            filtered_df.shape[0],
        )

        return filtered_df

    except TypeError:
        logger.exception("Invalid input type while filtering countries.")
        raise
    except KeyError:
        logger.exception("Missing required columns while filtering countries.")
        raise
    except ValueError:
        logger.exception("Invalid country filter.")
        raise
    except Exception:
        logger.exception("Unexpected error while filtering countries.")
        raise


def filter_indicator(
    df: pd.DataFrame,
    indicator_code: str | None = None,
) -> pd.DataFrame:
    """
    Filter a metrics DataFrame by an optional indicator code.

    Args:
        df: Metrics DataFrame.
        indicator_code: Optional indicator code.

    Returns:
        Filtered DataFrame.

    Raises:
        TypeError: If df is not a pandas DataFrame.
        KeyError: If required columns are missing.
        ValueError: If the indicator is invalid or not found.
        Exception: For unexpected errors.
    """
    logger.info("Filtering DataFrame by indicator.")

    try:
        _validate_dataframe(df)
        _validate_required_columns(df)

        if indicator_code is None:
            logger.info("No indicator filter applied.")
            return df.copy().reset_index(drop=True)

        normalized_indicator = _normalize_code(indicator_code, "indicator_code")

        filtered_df = df[
            df[INDICATOR_CODE_COLUMN]
            .astype(str)
            .str.strip()
            .str.upper()
            .eq(normalized_indicator)
        ].copy()

        filtered_df = filtered_df.reset_index(drop=True)

        if filtered_df.empty:
            raise ValueError(
                f"No records found for indicator_code '{normalized_indicator}'."
            )

        logger.info(
            "Filtered indicator '%s'. Rows after filter: %s",
            normalized_indicator,
            filtered_df.shape[0],
        )

        return filtered_df

    except TypeError:
        logger.exception("Invalid input type while filtering indicator.")
        raise
    except KeyError:
        logger.exception("Missing required columns while filtering indicator.")
        raise
    except ValueError:
        logger.exception("Invalid indicator filter.")
        raise
    except Exception:
        logger.exception("Unexpected error while filtering indicator.")
        raise


def compare_countries(
    df: pd.DataFrame,
    countries: list[str],
    indicator_code: str | None = None,
) -> pd.DataFrame:
    """
    Compare selected countries by indicator using final values and metrics.

    Args:
        df: Metrics DataFrame.
        countries: List of country codes to compare.
        indicator_code: Optional indicator code to filter.

    Returns:
        Comparative DataFrame with leader and lowest performer information.

    Raises:
        TypeError: If inputs have invalid types.
        KeyError: If required columns are missing.
        ValueError: If filters produce no valid records.
        Exception: For unexpected errors.
    """
    logger.info("Starting country comparison.")

    try:
        _validate_dataframe(df)
        _validate_required_columns(df)

        logger.info("Selected countries: %s", countries)
        if indicator_code is not None:
            logger.info("Selected indicator: %s", indicator_code)

        comparison_df = filter_countries(df, countries)
        comparison_df = filter_indicator(comparison_df, indicator_code)

        comparison_df[FINAL_VALUE_COLUMN] = pd.to_numeric(
            comparison_df[FINAL_VALUE_COLUMN],
            errors="coerce",
        )

        rows_before_dropna = comparison_df.shape[0]
        comparison_df = comparison_df.dropna(subset=[FINAL_VALUE_COLUMN])
        removed_rows = rows_before_dropna - comparison_df.shape[0]

        logger.info("Removed %s rows with missing final_value.", removed_rows)

        if comparison_df.empty:
            raise ValueError("No valid records available for comparison.")

        result_frames: list[pd.DataFrame] = []

        grouped = comparison_df.groupby(
            [INDICATOR_CODE_COLUMN, INDICATOR_NAME_COLUMN],
            dropna=False,
            sort=False,
        )

        logger.info("Comparing %s indicators.", grouped.ngroups)

        for _, group in grouped:
            group_df = group.copy().reset_index(drop=True)

            leader_row = group_df.sort_values(
                FINAL_VALUE_COLUMN,
                ascending=False,
            ).iloc[0]

            lowest_row = group_df.sort_values(
                FINAL_VALUE_COLUMN,
                ascending=True,
            ).iloc[0]

            leader_value = float(leader_row[FINAL_VALUE_COLUMN])
            lowest_value = float(lowest_row[FINAL_VALUE_COLUMN])

            group_df[LEADER_COUNTRY_COLUMN] = leader_row[COUNTRY_COLUMN]
            group_df[LEADER_COUNTRY_CODE_COLUMN] = leader_row[COUNTRY_CODE_COLUMN]
            group_df[LEADER_VALUE_COLUMN] = leader_value

            group_df[LOWEST_COUNTRY_COLUMN] = lowest_row[COUNTRY_COLUMN]
            group_df[LOWEST_COUNTRY_CODE_COLUMN] = lowest_row[COUNTRY_CODE_COLUMN]
            group_df[LOWEST_VALUE_COLUMN] = lowest_value

            group_df[DIFFERENCE_TO_LEADER_COLUMN] = (
                group_df[FINAL_VALUE_COLUMN] - leader_value
            )

            if pd.isna(leader_value) or leader_value == 0:
                group_df[PERCENTAGE_DIFFERENCE_TO_LEADER_COLUMN] = None
            else:
                group_df[PERCENTAGE_DIFFERENCE_TO_LEADER_COLUMN] = (
                    group_df[DIFFERENCE_TO_LEADER_COLUMN] / leader_value
                ) * 100

            result_frames.append(group_df)

        result_df = pd.concat(result_frames, ignore_index=True)
        result_df = result_df[FINAL_COLUMNS]

        result_df = result_df.sort_values(
            by=[
                INDICATOR_CODE_COLUMN,
                FINAL_VALUE_COLUMN,
            ],
            ascending=[
                True,
                False,
            ],
        ).reset_index(drop=True)

        logger.info("Country comparison completed. Final shape: %s", result_df.shape)
        return result_df

    except TypeError:
        logger.exception("Invalid input type during country comparison.")
        raise
    except KeyError:
        logger.exception("Missing required columns during country comparison.")
        raise
    except ValueError:
        logger.exception("Invalid value during country comparison.")
        raise
    except Exception:
        logger.exception("Unexpected error during country comparison.")
        raise