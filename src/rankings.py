import pandas as pd

from .utils import setup_logger


logger = setup_logger(__name__)

COUNTRY_COLUMN = "country"
COUNTRY_CODE_COLUMN = "country_code"
INDICATOR_CODE_COLUMN = "indicator_code"
INDICATOR_NAME_COLUMN = "indicator_name"
FINAL_VALUE_COLUMN = "final_value"
ABSOLUTE_GROWTH_COLUMN = "absolute_growth"
PERCENTAGE_GROWTH_COLUMN = "percentage_growth"
RANK_COLUMN = "rank"

VALID_RANKING_METRICS: list[str] = [
    FINAL_VALUE_COLUMN,
    ABSOLUTE_GROWTH_COLUMN,
    PERCENTAGE_GROWTH_COLUMN,
]

REQUIRED_COLUMNS: list[str] = [
    COUNTRY_COLUMN,
    COUNTRY_CODE_COLUMN,
    INDICATOR_CODE_COLUMN,
    INDICATOR_NAME_COLUMN,
    FINAL_VALUE_COLUMN,
    ABSOLUTE_GROWTH_COLUMN,
    PERCENTAGE_GROWTH_COLUMN,
]


def _validate_required_columns(
    df: pd.DataFrame,
    required_columns: list[str],
) -> None:
    """
    Validate that required columns exist in the DataFrame.

    Args:
        df: DataFrame to validate.
        required_columns: List of required column names.

    Raises:
        KeyError: If one or more required columns are missing.
    """
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")


def _validate_ranking_metric(metric: str) -> None:
    """
    Validate ranking metric name.

    Args:
        metric: Metric column name to validate.

    Raises:
        TypeError: If metric is not a string.
        ValueError: If metric is not a valid ranking metric.
    """
    if not isinstance(metric, str):
        raise TypeError("metric must be a string.")

    if metric not in VALID_RANKING_METRICS:
        raise ValueError(
            f"Invalid ranking metric '{metric}'. "
            f"Valid options are: {VALID_RANKING_METRICS}"
        )


def _validate_positive_integer(value: int, name: str) -> None:
    """
    Validate that a value is a positive integer.

    Args:
        value: Value to validate.
        name: Name of the value for error messages.

    Raises:
        TypeError: If value is not an integer.
        ValueError: If value is not positive.
    """
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")

    if value <= 0:
        raise ValueError(f"{name} must be a positive integer.")


def _normalize_indicator_code(indicator_code: str) -> str:
    """
    Normalize an indicator code by removing spaces and converting to uppercase.

    Args:
        indicator_code: Indicator code to normalize.

    Returns:
        Normalized indicator code.

    Raises:
        ValueError: If indicator_code is empty.
    """
    normalized_indicator_code = indicator_code.strip().upper()

    if not normalized_indicator_code:
        raise ValueError("indicator_code must be a non-empty string.")

    return normalized_indicator_code


def filter_by_indicator(
    df: pd.DataFrame,
    indicator_code: str | None = None,
) -> pd.DataFrame:
    """
    Filter metrics DataFrame by indicator code.

    Args:
        df: Metrics DataFrame.
        indicator_code: Optional indicator code to filter.

    Returns:
        Filtered DataFrame.

    Raises:
        TypeError: If df is not a pandas DataFrame.
        KeyError: If required columns are missing.
        ValueError: If no rows are found for the indicator.
        Exception: For unexpected errors.
    """
    logger.info("Filtering DataFrame by indicator.")

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        _validate_required_columns(df, REQUIRED_COLUMNS)

        if indicator_code is None:
            logger.info("No indicator filter applied.")
            return df.copy().reset_index(drop=True)

        if not isinstance(indicator_code, str):
            raise TypeError("indicator_code must be a string or None.")

        normalized_indicator_code = _normalize_indicator_code(indicator_code)

        filtered_df = df[
            df[INDICATOR_CODE_COLUMN]
            .astype(str)
            .str.strip()
            .str.upper()
            .eq(normalized_indicator_code)
        ].copy()

        filtered_df = filtered_df.reset_index(drop=True)

        if filtered_df.empty:
            raise ValueError(
                f"No records found for indicator_code '{normalized_indicator_code}'."
            )

        logger.info(
            "Filtered DataFrame by indicator '%s'. Rows: %s",
            normalized_indicator_code,
            filtered_df.shape[0],
        )

        return filtered_df

    except TypeError:
        logger.exception("Invalid input type while filtering by indicator.")
        raise
    except KeyError:
        logger.exception("Missing required columns while filtering by indicator.")
        raise
    except ValueError:
        logger.exception("Invalid indicator filter.")
        raise
    except Exception:
        logger.exception("Unexpected error while filtering by indicator.")
        raise


def generate_ranking(
    df: pd.DataFrame,
    metric: str = FINAL_VALUE_COLUMN,
    indicator_code: str | None = None,
    ascending: bool = False,
) -> pd.DataFrame:
    """
    Generate a ranking based on a selected metric.

    Args:
        df: Metrics DataFrame.
        metric: Metric column used for ranking.
        indicator_code: Optional indicator code to filter.
        ascending: Whether to sort in ascending order.

    Returns:
        Ranking DataFrame.

    Raises:
        TypeError: If inputs have invalid types.
        KeyError: If required columns are missing.
        ValueError: If metric or indicator filter is invalid.
        Exception: For unexpected errors.
    """
    logger.info("Generating ranking.")

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        if not isinstance(ascending, bool):
            raise TypeError("ascending must be a boolean.")

        _validate_required_columns(df, REQUIRED_COLUMNS)
        _validate_ranking_metric(metric)

        ranking_df = filter_by_indicator(df, indicator_code)
        logger.info("Ranking metric: %s", metric)

        ranking_df[metric] = pd.to_numeric(ranking_df[metric], errors="coerce")
        ranking_df = ranking_df.dropna(subset=[metric])

        ranking_df = ranking_df.sort_values(
            by=metric,
            ascending=ascending,
        ).reset_index(drop=True)

        ranking_df[RANK_COLUMN] = range(1, len(ranking_df) + 1)

        logger.info("Ranking generated. Rows: %s", ranking_df.shape[0])
        return ranking_df

    except TypeError:
        logger.exception("Invalid input type while generating ranking.")
        raise
    except KeyError:
        logger.exception("Missing required columns while generating ranking.")
        raise
    except ValueError:
        logger.exception("Invalid value while generating ranking.")
        raise
    except Exception:
        logger.exception("Unexpected error while generating ranking.")
        raise


def rank_by_final_value(
    df: pd.DataFrame,
    indicator_code: str | None = None,
    ascending: bool = False,
) -> pd.DataFrame:
    """
    Generate ranking by final value.

    Args:
        df: Metrics DataFrame.
        indicator_code: Optional indicator code to filter.
        ascending: Whether to sort in ascending order.

    Returns:
        Ranking DataFrame sorted by final value.
    """
    return generate_ranking(
        df=df,
        metric=FINAL_VALUE_COLUMN,
        indicator_code=indicator_code,
        ascending=ascending,
    )


def rank_by_absolute_growth(
    df: pd.DataFrame,
    indicator_code: str | None = None,
    ascending: bool = False,
) -> pd.DataFrame:
    """
    Generate ranking by absolute growth.

    Args:
        df: Metrics DataFrame.
        indicator_code: Optional indicator code to filter.
        ascending: Whether to sort in ascending order.

    Returns:
        Ranking DataFrame sorted by absolute growth.
    """
    return generate_ranking(
        df=df,
        metric=ABSOLUTE_GROWTH_COLUMN,
        indicator_code=indicator_code,
        ascending=ascending,
    )


def rank_by_percentage_growth(
    df: pd.DataFrame,
    indicator_code: str | None = None,
    ascending: bool = False,
) -> pd.DataFrame:
    """
    Generate ranking by percentage growth.

    Args:
        df: Metrics DataFrame.
        indicator_code: Optional indicator code to filter.
        ascending: Whether to sort in ascending order.

    Returns:
        Ranking DataFrame sorted by percentage growth.
    """
    return generate_ranking(
        df=df,
        metric=PERCENTAGE_GROWTH_COLUMN,
        indicator_code=indicator_code,
        ascending=ascending,
    )


def get_top_n(
    df: pd.DataFrame,
    metric: str = FINAL_VALUE_COLUMN,
    n: int = 10,
    indicator_code: str | None = None,
) -> pd.DataFrame:
    """
    Return the top N countries based on a ranking metric.

    Args:
        df: Metrics DataFrame.
        metric: Metric column used for ranking.
        n: Number of rows to return.
        indicator_code: Optional indicator code to filter.

    Returns:
        Top N ranking DataFrame.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is not positive.
    """
    logger.info("Generating Top %s ranking.", n)

    try:
        _validate_positive_integer(n, "n")

        top_df = generate_ranking(
            df=df,
            metric=metric,
            indicator_code=indicator_code,
            ascending=False,
        ).head(n)

        logger.info("Top %s ranking generated. Rows: %s", n, top_df.shape[0])
        return top_df.reset_index(drop=True)

    except TypeError:
        logger.exception("Invalid input type while generating Top N ranking.")
        raise
    except KeyError:
        logger.exception("Missing required columns while generating Top N ranking.")
        raise
    except ValueError:
        logger.exception("Invalid value while generating Top N ranking.")
        raise
    except Exception:
        logger.exception("Unexpected error while generating Top N ranking.")
        raise


def get_bottom_n(
    df: pd.DataFrame,
    metric: str = FINAL_VALUE_COLUMN,
    n: int = 10,
    indicator_code: str | None = None,
) -> pd.DataFrame:
    """
    Return the bottom N countries based on a ranking metric.

    Args:
        df: Metrics DataFrame.
        metric: Metric column used for ranking.
        n: Number of rows to return.
        indicator_code: Optional indicator code to filter.

    Returns:
        Bottom N ranking DataFrame.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is not positive.
    """
    logger.info("Generating Bottom %s ranking.", n)

    try:
        _validate_positive_integer(n, "n")

        bottom_df = generate_ranking(
            df=df,
            metric=metric,
            indicator_code=indicator_code,
            ascending=True,
        ).head(n)

        logger.info("Bottom %s ranking generated. Rows: %s", n, bottom_df.shape[0])
        return bottom_df.reset_index(drop=True)

    except TypeError:
        logger.exception("Invalid input type while generating Bottom N ranking.")
        raise
    except KeyError:
        logger.exception("Missing required columns while generating Bottom N ranking.")
        raise
    except ValueError:
        logger.exception("Invalid value while generating Bottom N ranking.")
        raise
    except Exception:
        logger.exception("Unexpected error while generating Bottom N ranking.")
        raise