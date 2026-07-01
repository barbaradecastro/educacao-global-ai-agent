import pandas as pd

from .utils import setup_logger, validate_indicators


logger = setup_logger(__name__)

INDICATOR_CODE_COLUMN = "indicator_code"
INDICATOR_NAME_COLUMN = "indicator_name"

REQUIRED_COLUMNS: list[str] = [
    INDICATOR_CODE_COLUMN,
    INDICATOR_NAME_COLUMN,
]


def _validate_required_columns(df: pd.DataFrame) -> None:
    """
    Validate that the required indicator columns exist.

    Args:
        df: DataFrame to validate.

    Raises:
        KeyError: If one or more required columns are missing.
    """
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")


def _normalize_indicators(indicators: list[str]) -> list[str]:
    """
    Normalize indicator codes to uppercase and remove extra spaces.

    Args:
        indicators: List of indicator codes.

    Returns:
        Normalized list of indicator codes.
    """
    return [indicator.strip().upper() for indicator in indicators]


def list_available_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    List unique indicators available in the DataFrame.

    Args:
        df: DataFrame containing indicator columns.

    Returns:
        DataFrame with unique indicator codes and names.

    Raises:
        TypeError: If df is not a pandas DataFrame.
        KeyError: If required columns are missing.
        Exception: For unexpected errors.
    """
    logger.info("Listing available indicators.")

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        _validate_required_columns(df)

        indicators_df = (
            df[REQUIRED_COLUMNS]
            .dropna(subset=REQUIRED_COLUMNS)
            .drop_duplicates()
            .sort_values(INDICATOR_CODE_COLUMN)
            .reset_index(drop=True)
        )

        logger.info("Found %s available indicators.", indicators_df.shape[0])
        return indicators_df

    except TypeError:
        logger.exception("Invalid input type while listing indicators.")
        raise
    except KeyError:
        logger.exception("Missing required columns while listing indicators.")
        raise
    except Exception:
        logger.exception("Unexpected error while listing indicators.")
        raise


def validate_selected_indicators(
    df: pd.DataFrame,
    indicators: list[str],
) -> None:
    """
    Validate that selected indicators exist in the DataFrame.

    Args:
        df: DataFrame containing indicator codes.
        indicators: List of indicator codes selected by the user.

    Raises:
        TypeError: If df or indicators have invalid types.
        KeyError: If required columns are missing.
        ValueError: If one or more indicators are invalid.
        Exception: For unexpected errors.
    """
    logger.info("Validating selected indicators.")

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        validate_indicators(indicators)
        _validate_required_columns(df)

        normalized_indicators = _normalize_indicators(indicators)

        available_indicators = {
            indicator.strip().upper()
            for indicator in df[INDICATOR_CODE_COLUMN].dropna().astype(str)
        }

        invalid_indicators = [
            indicator
            for indicator in normalized_indicators
            if indicator not in available_indicators
        ]

        if invalid_indicators:
            logger.error("Invalid indicators found: %s", invalid_indicators)
            raise ValueError(f"Invalid indicators: {invalid_indicators}")

        logger.info("Selected indicators validated successfully.")

    except TypeError:
        logger.exception("Invalid input type while validating selected indicators.")
        raise
    except KeyError:
        logger.exception("Missing required columns while validating selected indicators.")
        raise
    except ValueError:
        logger.exception("Invalid indicators selected.")
        raise
    except Exception:
        logger.exception("Unexpected error while validating selected indicators.")
        raise


def map_indicator_names(df: pd.DataFrame) -> dict[str, str]:
    """
    Map indicator codes to friendly indicator names.

    Args:
        df: DataFrame containing indicator codes and names.

    Returns:
        Dictionary mapping indicator_code to indicator_name.

    Raises:
        TypeError: If df is not a pandas DataFrame.
        KeyError: If required columns are missing.
        Exception: For unexpected errors.
    """
    logger.info("Mapping indicator codes to names.")

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        _validate_required_columns(df)

        mapping_df = (
            df[REQUIRED_COLUMNS]
            .dropna(subset=REQUIRED_COLUMNS)
            .drop_duplicates(subset=[INDICATOR_CODE_COLUMN], keep="first")
            .sort_values(INDICATOR_CODE_COLUMN)
        )

        indicator_mapping = dict(
            zip(
                mapping_df[INDICATOR_CODE_COLUMN],
                mapping_df[INDICATOR_NAME_COLUMN],
            )
        )

        logger.info("Mapped %s indicator names.", len(indicator_mapping))
        return indicator_mapping

    except TypeError:
        logger.exception("Invalid input type while mapping indicator names.")
        raise
    except KeyError:
        logger.exception("Missing required columns while mapping indicator names.")
        raise
    except Exception:
        logger.exception("Unexpected error while mapping indicator names.")
        raise


def filter_indicators(
    df: pd.DataFrame,
    indicators: list[str],
) -> pd.DataFrame:
    """
    Filter DataFrame rows by selected indicator codes.

    Args:
        df: DataFrame containing indicator codes.
        indicators: List of indicator codes to filter.

    Returns:
        Filtered DataFrame containing only selected indicators.

    Raises:
        TypeError: If df or indicators have invalid types.
        KeyError: If required columns are missing.
        ValueError: If one or more indicators are invalid.
        Exception: For unexpected errors.
    """
    logger.info("Filtering DataFrame by indicators.")

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        validate_selected_indicators(df, indicators)

        normalized_indicators = _normalize_indicators(indicators)

        filtered_df = df[
            df[INDICATOR_CODE_COLUMN]
            .astype(str)
            .str.strip()
            .str.upper()
            .isin(normalized_indicators)
        ].copy()

        sort_columns = [
            column
            for column in ["country", INDICATOR_CODE_COLUMN, "year"]
            if column in filtered_df.columns
        ]

        if sort_columns:
            filtered_df = filtered_df.sort_values(by=sort_columns)

        filtered_df = filtered_df.reset_index(drop=True)

        logger.info("Filtered DataFrame shape: %s", filtered_df.shape)
        return filtered_df

    except TypeError:
        logger.exception("Invalid input type while filtering indicators.")
        raise
    except KeyError:
        logger.exception("Missing required columns while filtering indicators.")
        raise
    except ValueError:
        logger.exception("Invalid indicators while filtering DataFrame.")
        raise
    except Exception:
        logger.exception("Unexpected error while filtering indicators.")
        raise