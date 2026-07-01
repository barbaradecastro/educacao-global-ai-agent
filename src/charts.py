from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .config import CHARTS_DIR
from .utils import setup_logger


logger = setup_logger(__name__)

COUNTRY_COLUMN = "country"
COUNTRY_CODE_COLUMN = "country_code"
YEAR_COLUMN = "year"
VALUE_COLUMN = "value"
RANK_COLUMN = "rank"
FINAL_VALUE_COLUMN = "final_value"
INDICATOR_CODE_COLUMN = "indicator_code"
INDICATOR_NAME_COLUMN = "indicator_name"


def _ensure_charts_directory() -> None:
    """Create the charts output directory if it does not exist."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)


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


def create_ranking_bar_chart(
    df: pd.DataFrame,
    value_column: str = FINAL_VALUE_COLUMN,
    title: str = "Ranking",
    filename: str = "ranking.png",
) -> Path:
    """
    Create and save a ranking bar chart as a PNG file.

    Args:
        df: Ranking DataFrame.
        value_column: Column to use as bar values.
        title: Chart title.
        filename: Output PNG filename.

    Returns:
        Path to the generated PNG file.
    """
    logger.info("Starting ranking bar chart generation.")

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        if not isinstance(value_column, str) or not value_column.strip():
            raise ValueError("value_column must be a non-empty string.")

        if not isinstance(title, str):
            raise TypeError("title must be a string.")

        if not isinstance(filename, str) or not filename.strip():
            raise ValueError("filename must be a non-empty string.")

        _validate_required_columns(df, [COUNTRY_COLUMN, value_column])

        chart_df = df.copy()
        chart_df[value_column] = pd.to_numeric(
            chart_df[value_column],
            errors="coerce",
        )
        chart_df = chart_df.dropna(subset=[value_column])

        if chart_df.empty:
            raise ValueError("No valid data available to create ranking bar chart.")

        _ensure_charts_directory()
        output_path = CHARTS_DIR / filename

        logger.info(
            "Generating ranking bar chart with %s records.",
            chart_df.shape[0],
        )

        plt.figure(figsize=(12, 6))
        plt.bar(chart_df[COUNTRY_COLUMN].astype(str), chart_df[value_column])
        plt.title(title)
        plt.xlabel("Country")
        plt.ylabel(value_column)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(output_path, format="png")
        plt.close()

        logger.info("Ranking bar chart saved to: %s", output_path)
        return output_path

    except TypeError:
        logger.exception("Invalid input type while creating ranking bar chart.")
        raise
    except KeyError:
        logger.exception("Missing required columns while creating ranking bar chart.")
        raise
    except ValueError:
        logger.exception("Invalid value while creating ranking bar chart.")
        raise
    except OSError:
        logger.exception("Failed to save ranking bar chart.")
        raise
    except Exception:
        logger.exception("Unexpected error while creating ranking bar chart.")
        raise


def create_time_series_chart(
    df: pd.DataFrame,
    title: str = "Historical Evolution",
    filename: str = "timeseries.png",
) -> Path:
    """
    Create and save a time series line chart as a PNG file.

    Args:
        df: Long-format DataFrame containing historical values.
        title: Chart title.
        filename: Output PNG filename.

    Returns:
        Path to the generated PNG file.
    """
    logger.info("Starting time series chart generation.")

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        if not isinstance(title, str):
            raise TypeError("title must be a string.")

        if not isinstance(filename, str) or not filename.strip():
            raise ValueError("filename must be a non-empty string.")

        _validate_required_columns(df, [COUNTRY_COLUMN, YEAR_COLUMN, VALUE_COLUMN])

        chart_df = df.copy()
        chart_df[YEAR_COLUMN] = pd.to_numeric(chart_df[YEAR_COLUMN], errors="coerce")
        chart_df[VALUE_COLUMN] = pd.to_numeric(chart_df[VALUE_COLUMN], errors="coerce")
        chart_df = chart_df.dropna(subset=[COUNTRY_COLUMN, YEAR_COLUMN, VALUE_COLUMN])

        if chart_df.empty:
            raise ValueError("No valid data available to create time series chart.")

        chart_df[YEAR_COLUMN] = chart_df[YEAR_COLUMN].astype(int)
        chart_df = chart_df.sort_values([COUNTRY_COLUMN, YEAR_COLUMN])

        _ensure_charts_directory()
        output_path = CHARTS_DIR / filename

        logger.info(
            "Generating time series chart with %s records.",
            chart_df.shape[0],
        )

        plt.figure(figsize=(12, 6))

        for country, country_df in chart_df.groupby(COUNTRY_COLUMN):
            plt.plot(
                country_df[YEAR_COLUMN],
                country_df[VALUE_COLUMN],
                marker="o",
                label=str(country),
            )

        plt.title(title)
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_path, format="png")
        plt.close()

        logger.info("Time series chart saved to: %s", output_path)
        return output_path

    except TypeError:
        logger.exception("Invalid input type while creating time series chart.")
        raise
    except KeyError:
        logger.exception("Missing required columns while creating time series chart.")
        raise
    except ValueError:
        logger.exception("Invalid value while creating time series chart.")
        raise
    except OSError:
        logger.exception("Failed to save time series chart.")
        raise
    except Exception:
        logger.exception("Unexpected error while creating time series chart.")
        raise