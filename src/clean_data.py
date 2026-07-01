import pandas as pd

from .config import EDUCATION_CLEAN_FILE
from .utils import setup_logger


logger = setup_logger(__name__)

REQUIRED_COLUMNS: list[str] = [
    "Country Name",
    "Country Code",
    "Indicator Name",
    "Indicator Code",
]


def _validate_required_columns(df: pd.DataFrame) -> None:
    """
    Validate that all required EdStats columns exist.

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


def _standardize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize text fields used by the EdStats dataset.

    Args:
        df: DataFrame to standardize.

    Returns:
        DataFrame with standardized text columns.
    """
    cleaned_df = df.copy()

    cleaned_df["Country Name"] = cleaned_df["Country Name"].astype(str).str.strip()
    cleaned_df["Country Code"] = (
        cleaned_df["Country Code"].astype(str).str.strip().str.upper()
    )
    cleaned_df["Indicator Name"] = cleaned_df["Indicator Name"].astype(str).str.strip()
    cleaned_df["Indicator Code"] = (
        cleaned_df["Indicator Code"].astype(str).str.strip().str.upper()
    )

    return cleaned_df


def _convert_year_columns(
    df: pd.DataFrame,
    year_columns: list[str],
) -> pd.DataFrame:
    """
    Convert year columns to numeric values.

    Args:
        df: DataFrame containing year columns.
        year_columns: List of columns that represent years.

    Returns:
        DataFrame with numeric year columns.
    """
    cleaned_df = df.copy()

    for column in year_columns:
        cleaned_df[column] = pd.to_numeric(cleaned_df[column], errors="coerce")

    return cleaned_df


def clean_education_data(
    df: pd.DataFrame,
    save_output: bool = True,
) -> pd.DataFrame:
    """
    Clean the main EdStats education DataFrame.

    Args:
        df: Raw EdStats education DataFrame.
        save_output: Whether to save the cleaned DataFrame to disk.

    Returns:
        Cleaned pandas DataFrame.

    Raises:
        TypeError: If df is not a pandas DataFrame.
        KeyError: If required columns are missing.
        ValueError: If cleaning produces invalid results.
        OSError: If the cleaned file cannot be saved.
        Exception: For unexpected errors during cleaning.
    """
    logger.info("Starting education data cleaning.")

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        logger.info("Initial DataFrame shape: %s", df.shape)

        cleaned_df = df.copy()

        initial_columns = cleaned_df.shape[1]
        cleaned_df = cleaned_df.dropna(axis=1, how="all")
        removed_empty_columns = initial_columns - cleaned_df.shape[1]
        logger.info("Removed %s fully empty columns.", removed_empty_columns)

        _validate_required_columns(cleaned_df)

        initial_rows = cleaned_df.shape[0]
        cleaned_df = cleaned_df.dropna(subset=REQUIRED_COLUMNS)
        removed_invalid_rows = initial_rows - cleaned_df.shape[0]
        logger.info("Removed %s rows missing required fields.", removed_invalid_rows)

        cleaned_df = _standardize_text_columns(cleaned_df)

        year_columns = _get_year_columns(cleaned_df)
        logger.info("Identified %s year columns.", len(year_columns))

        cleaned_df = _convert_year_columns(cleaned_df, year_columns)
        logger.info("Converted %s year columns to numeric.", len(year_columns))

        if year_columns:
            rows_before_year_filter = cleaned_df.shape[0]
            cleaned_df = cleaned_df.dropna(subset=year_columns, how="all")
            removed_empty_year_rows = rows_before_year_filter - cleaned_df.shape[0]
            logger.info(
                "Removed %s rows with all year values missing.",
                removed_empty_year_rows,
            )

        if cleaned_df.empty:
            raise ValueError("Cleaned DataFrame is empty.")

        if save_output:
            EDUCATION_CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
            cleaned_df.to_csv(EDUCATION_CLEAN_FILE, index=False, encoding="utf-8")
            logger.info("Cleaned data saved to: %s", EDUCATION_CLEAN_FILE)

        logger.info("Education data cleaning completed. Final shape: %s", cleaned_df.shape)
        return cleaned_df

    except KeyError:
        logger.exception("Missing required columns during education data cleaning.")
        raise
    except TypeError:
        logger.exception("Invalid input type during education data cleaning.")
        raise
    except ValueError:
        logger.exception("Invalid value encountered during education data cleaning.")
        raise
    except OSError:
        logger.exception("Failed to save cleaned education data.")
        raise
    except Exception:
        logger.exception("Unexpected error during education data cleaning.")
        raise