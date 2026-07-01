from pathlib import Path

import pandas as pd

from .config import (
    EDSTATS_COUNTRY_FILE,
    EDSTATS_DATA_FILE,
    EDSTATS_FOOTNOTE_FILE,
    EDSTATS_SERIES_FILE,
    validate_raw_files,
)
from .utils import setup_logger


logger = setup_logger(__name__)


def _read_csv(file_path: Path) -> pd.DataFrame:
    """
    Read a CSV file using a standard encoding with fallback.

    Args:
        file_path: Path to the CSV file.

    Returns:
        Loaded pandas DataFrame.

    Raises:
        UnicodeDecodeError: If decoding fails with supported encodings.
        pandas.errors.ParserError: If pandas cannot parse the CSV file.
        OSError: If the file cannot be accessed.
    """
    logger.info("Loading CSV file: %s", file_path)

    try:
        return pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        logger.warning(
            "UTF-8 decoding failed for %s. Retrying with latin-1.",
            file_path,
        )
        return pd.read_csv(file_path, encoding="latin-1")


def load_edstats_data() -> dict[str, pd.DataFrame]:
    """
    Load all raw EdStats dataset files.

    Returns:
        Dictionary containing the loaded DataFrames with the keys:
        data, country, series and footnote.

    Raises:
        FileNotFoundError: If one or more required raw files are missing.
        pandas.errors.ParserError: If any CSV file cannot be parsed.
        OSError: If any file cannot be accessed.
        Exception: For unexpected errors during loading.
    """
    logger.info("Starting EdStats raw data loading.")
    logger.info("Validating required raw files.")

    missing_files = validate_raw_files()

    if missing_files:
        missing_files_message = "\n".join(f"- {file_path.name}" for file_path in missing_files)
        error_message = f"Missing required raw dataset files:\n{missing_files_message}"
        logger.error(error_message)
        raise FileNotFoundError(error_message)

    try:
        datasets = {
            "data": _read_csv(EDSTATS_DATA_FILE),
            "country": _read_csv(EDSTATS_COUNTRY_FILE),
            "series": _read_csv(EDSTATS_SERIES_FILE),
            "footnote": _read_csv(EDSTATS_FOOTNOTE_FILE),
        }

        logger.info("Successfully loaded all EdStats raw data files.")
        return datasets

    except FileNotFoundError:
        logger.exception("A required raw data file was not found during loading.")
        raise
    except pd.errors.ParserError:
        logger.exception("Failed to parse one or more EdStats CSV files.")
        raise
    except UnicodeDecodeError:
        logger.exception("Failed to decode one or more EdStats CSV files.")
        raise
    except OSError:
        logger.exception("Failed to access one or more EdStats CSV files.")
        raise
    except Exception:
        logger.exception("Unexpected error while loading EdStats data.")
        raise