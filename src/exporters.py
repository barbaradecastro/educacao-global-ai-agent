import json
from pathlib import Path
from typing import Any

import pandas as pd

from .utils import setup_logger


logger = setup_logger(__name__)


def _prepare_output_path(output_path: str | Path) -> Path:
    """
    Prepare an output path by converting it to Path and creating parent directories.

    Args:
        output_path: Output file path.

    Returns:
        Prepared output path.

    Raises:
        TypeError: If output_path is not a string or Path.
        ValueError: If output_path is empty.
        OSError: If the parent directory cannot be created.
    """
    if not isinstance(output_path, (str, Path)):
        raise TypeError("output_path must be a string or pathlib.Path.")

    path = Path(output_path)

    if not str(path).strip():
        raise ValueError("output_path cannot be empty.")

    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def export_dataframe_to_csv(
    df: pd.DataFrame,
    output_path: str | Path,
) -> Path:
    """
    Export a pandas DataFrame to a CSV file.

    Args:
        df: DataFrame to export.
        output_path: Destination CSV file path.

    Returns:
        Path to the saved CSV file.

    Raises:
        TypeError: If df or output_path has an invalid type.
        ValueError: If output_path is invalid.
        OSError: If the file cannot be written.
        Exception: For unexpected errors.
    """
    logger.info("Starting CSV export.")

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        path = _prepare_output_path(output_path)

        logger.info(
            "Exporting DataFrame to CSV. Shape: %s. Output: %s",
            df.shape,
            path,
        )

        df.copy().to_csv(path, index=False, encoding="utf-8")

        logger.info("CSV export completed successfully: %s", path)
        return path

    except TypeError:
        logger.exception("Invalid input type during CSV export.")
        raise
    except ValueError:
        logger.exception("Invalid value during CSV export.")
        raise
    except OSError:
        logger.exception("Failed to write CSV file.")
        raise
    except Exception:
        logger.exception("Unexpected error during CSV export.")
        raise


def export_to_json(
    data: dict[str, Any] | list[Any],
    output_path: str | Path,
) -> Path:
    """
    Export a dictionary or list to a JSON file.

    Args:
        data: Dictionary or list to export.
        output_path: Destination JSON file path.

    Returns:
        Path to the saved JSON file.

    Raises:
        TypeError: If data or output_path has an invalid type.
        ValueError: If output_path is invalid.
        OSError: If the file cannot be written.
        Exception: For unexpected errors.
    """
    logger.info("Starting JSON export.")

    try:
        if not isinstance(data, (dict, list)):
            raise TypeError("data must be a dictionary or list.")

        path = _prepare_output_path(output_path)

        logger.info("Exporting data to JSON. Output: %s", path)

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        logger.info("JSON export completed successfully: %s", path)
        return path

    except TypeError:
        logger.exception("Invalid input type during JSON export.")
        raise
    except ValueError:
        logger.exception("Invalid value during JSON export.")
        raise
    except OSError:
        logger.exception("Failed to write JSON file.")
        raise
    except Exception:
        logger.exception("Unexpected error during JSON export.")
        raise


def export_markdown(
    markdown_text: str,
    output_path: str | Path,
) -> Path:
    """
    Export Markdown text to a .md file.

    Args:
        markdown_text: Markdown content to export.
        output_path: Destination Markdown file path.

    Returns:
        Path to the saved Markdown file.

    Raises:
        TypeError: If markdown_text or output_path has an invalid type.
        ValueError: If output_path is invalid.
        OSError: If the file cannot be written.
        Exception: For unexpected errors.
    """
    logger.info("Starting Markdown export.")

    try:
        if not isinstance(markdown_text, str):
            raise TypeError("markdown_text must be a string.")

        path = _prepare_output_path(output_path)

        logger.info("Exporting Markdown to file. Output: %s", path)

        with path.open("w", encoding="utf-8") as file:
            file.write(markdown_text)

        logger.info("Markdown export completed successfully: %s", path)
        return path

    except TypeError:
        logger.exception("Invalid input type during Markdown export.")
        raise
    except ValueError:
        logger.exception("Invalid value during Markdown export.")
        raise
    except OSError:
        logger.exception("Failed to write Markdown file.")
        raise
    except Exception:
        logger.exception("Unexpected error during Markdown export.")
        raise