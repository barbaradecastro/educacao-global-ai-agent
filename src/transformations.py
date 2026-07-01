import pandas as pd

from .utils import setup_logger, validate_year_range


logger = setup_logger(__name__)

REQUIRED_COLUMNS: list[str] = [
    "Country Name",
    "Country Code",
    "Indicator Code",
    "Indicator Name",
]

COLUMN_MAPPING: dict[str, str] = {
    "Country Name": "country",
    "Country Code": "country_code",
    "Indicator Code": "indicator_code",
    "Indicator Name": "indicator_name",
}

FINAL_COLUMNS: list[str] = [
    "country",
    "country_code",
    "indicator_code",
    "indicator_name",
    "year",
    "value",
]


def _validate_required_columns(df: pd.DataFrame) -> None:
    """
    Validate that the required EdStats columns exist.

    Args:
        df: DataFrame to validate.

    Raises:
        KeyError: If one or more required columns are missing.
    """
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")


def _get_year_columns(df: pd.DataFrame) -> list[str]:
    """
    Identify columns whose names represent years.

    Args:
        df: DataFrame containing EdStats columns.

    Returns:
        List of column names that represent years.
    """
    return [column for column in df.columns if str(column).strip().isdigit()]


def _warn_if_year_range_exceeds_available_data(
    year_columns: list[str],
    start_year: int,
    end_year: int,
) -> None:
    """
    Log warnings when the requested period is outside available year columns.

    Args:
        year_columns: List of columns representing available years.
        start_year: Initial requested year.
        end_year: Final requested year.
    """
    available_years = [int(column) for column in year_columns]

    min_available_year = min(available_years)
    max_available_year = max(available_years)

    if start_year < min_available_year:
        logger.warning(
            "Requested start_year %s is earlier than the first available year %s.",
            start_year,
            min_available_year,
        )

    if end_year > max_available_year:
        logger.warning(
            "Requested end_year %s is later than the last available year %s.",
            end_year,
            max_available_year,
        )


def transform_to_long_format(
    df: pd.DataFrame,
    start_year: int,
    end_year: int,
) -> pd.DataFrame:
    """
    Transform EdStats data from wide format to long analytical format.

    Args:
        df: Cleaned EdStats DataFrame in wide format.
        start_year: Initial year for filtering.
        end_year: Final year for filtering.

    Returns:
        DataFrame prepared for analysis with standardized columns.

    Raises:
        TypeError: If df is not a pandas DataFrame or years are invalid types.
        KeyError: If required columns are missing.
        ValueError: If year range is invalid or no year columns are found.
        Exception: For unexpected errors during transformation.
    """
    logger.info("Starting transformation to long format.")

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        validate_year_range(start_year, end_year)

        logger.info("Initial DataFrame shape: %s", df.shape)

        _validate_required_columns(df)

        year_columns = _get_year_columns(df)
        logger.info("Identified %s year columns.", len(year_columns))

        if not year_columns:
            raise ValueError("No year columns found in DataFrame.")

        _warn_if_year_range_exceeds_available_data(
            year_columns=year_columns,
            start_year=start_year,
            end_year=end_year,
        )

        transformed_df = pd.melt(
            df.copy(),
            id_vars=REQUIRED_COLUMNS,
            value_vars=year_columns,
            var_name="year",
            value_name="value",
        )

        logger.info("DataFrame shape after melt: %s", transformed_df.shape)

        transformed_df = transformed_df.rename(columns=COLUMN_MAPPING)

        transformed_df["year"] = transformed_df["year"].astype(int)
        transformed_df["value"] = pd.to_numeric(
            transformed_df["value"],
            errors="coerce",
        )

        transformed_df = transformed_df[
            (transformed_df["year"] >= start_year)
            & (transformed_df["year"] <= end_year)
        ]

        logger.info("Applied year filter from %s to %s.", start_year, end_year)

        rows_before_dropna = transformed_df.shape[0]
        transformed_df = transformed_df.dropna(subset=["value"])
        removed_missing_values = rows_before_dropna - transformed_df.shape[0]

        logger.info(
            "Removed %s rows with missing values.",
            removed_missing_values,
        )

        transformed_df = transformed_df[FINAL_COLUMNS]

        transformed_df = transformed_df.sort_values(
            by=[
                "country",
                "indicator_code",
                "year",
            ]
        ).reset_index(drop=True)

        logger.info(
            "Transformation to long format completed. Final shape: %s",
            transformed_df.shape,
        )

        return transformed_df

    except TypeError:
        logger.exception("Invalid input type during transformation.")
        raise
    except KeyError:
        logger.exception("Missing required columns during transformation.")
        raise
    except ValueError:
        logger.exception("Invalid value during transformation.")
        raise
    except Exception:
        logger.exception("Unexpected error during transformation.")
        raise