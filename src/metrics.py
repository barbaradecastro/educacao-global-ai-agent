import pandas as pd

from .utils import setup_logger


logger = setup_logger(__name__)

REQUIRED_COLUMNS: list[str] = [
    "country",
    "country_code",
    "indicator_code",
    "indicator_name",
    "year",
    "value",
]

METRICS_COLUMNS: list[str] = [
    "country",
    "country_code",
    "indicator_code",
    "indicator_name",
    "start_year",
    "end_year",
    "initial_value",
    "final_value",
    "historical_mean",
    "absolute_growth",
    "percentage_growth",
    "valid_observations",
    "trend",
]


def _validate_required_columns(df: pd.DataFrame) -> None:
    """
    Validate that all required columns exist in the DataFrame.

    Args:
        df: DataFrame to validate.

    Raises:
        KeyError: If one or more required columns are missing.
    """
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")


def _classify_trend(percentage_growth: float | None) -> str:
    """
    Classify trend based on percentage growth.

    Args:
        percentage_growth: Percentage growth between initial and final values.

    Returns:
        Trend classification.
    """
    if percentage_growth is None:
        return "indefinido"

    if percentage_growth > 5:
        return "crescimento"

    if percentage_growth < -5:
        return "queda"

    return "estabilidade"


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate analytical metrics by country and indicator.

    Args:
        df: Long-format EdStats DataFrame.

    Returns:
        DataFrame containing analytical metrics.

    Raises:
        TypeError: If df is not a pandas DataFrame.
        KeyError: If required columns are missing.
        ValueError: If invalid values prevent metric calculation.
        Exception: For unexpected errors.
    """
    logger.info("Starting metrics calculation.")

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        _validate_required_columns(df)

        logger.info("Initial DataFrame shape: %s", df.shape)

        metrics_df = df.copy()
        metrics_df["year"] = pd.to_numeric(metrics_df["year"], errors="coerce")
        metrics_df["value"] = pd.to_numeric(metrics_df["value"], errors="coerce")

        rows_before_dropna = metrics_df.shape[0]
        metrics_df = metrics_df.dropna(subset=["year", "value"])
        rows_removed = rows_before_dropna - metrics_df.shape[0]

        logger.info("Removed %s rows with missing year or value.", rows_removed)

        if metrics_df.empty:
            logger.warning("No valid data available for metrics calculation.")
            return pd.DataFrame(columns=METRICS_COLUMNS)

        metrics_df["year"] = metrics_df["year"].astype(int)

        metrics_df = metrics_df.sort_values(
            ["country_code", "indicator_code", "year"]
        ).reset_index(drop=True)

        grouped = metrics_df.groupby(
            ["country", "country_code", "indicator_code", "indicator_name"],
            dropna=False,
            sort=False,
        )

        logger.info("Processing %s country-indicator groups.", grouped.ngroups)

        records: list[dict[str, object]] = []

        for (
            country,
            country_code,
            indicator_code,
            indicator_name,
        ), group in grouped:
            ordered_group = group.sort_values("year")

            start_row = ordered_group.iloc[0]
            end_row = ordered_group.iloc[-1]

            start_year = int(start_row["year"])
            end_year = int(end_row["year"])
            initial_value = float(start_row["value"])
            final_value = float(end_row["value"])
            historical_mean = float(ordered_group["value"].mean())
            absolute_growth = final_value - initial_value

            if initial_value == 0:
                percentage_growth = None
            else:
                percentage_growth = (absolute_growth / initial_value) * 100

            records.append(
                {
                    "country": country,
                    "country_code": country_code,
                    "indicator_code": indicator_code,
                    "indicator_name": indicator_name,
                    "start_year": start_year,
                    "end_year": end_year,
                    "initial_value": initial_value,
                    "final_value": final_value,
                    "historical_mean": historical_mean,
                    "absolute_growth": absolute_growth,
                    "percentage_growth": percentage_growth,
                    "valid_observations": int(ordered_group["value"].count()),
                    "trend": _classify_trend(percentage_growth),
                }
            )

        result_df = pd.DataFrame(records, columns=METRICS_COLUMNS)

        logger.info("Metrics calculation completed. Final shape: %s", result_df.shape)
        return result_df

    except TypeError:
        logger.exception("Invalid input type during metrics calculation.")
        raise
    except KeyError:
        logger.exception("Missing required columns during metrics calculation.")
        raise
    except ValueError:
        logger.exception("Invalid value during metrics calculation.")
        raise
    except Exception:
        logger.exception("Unexpected error during metrics calculation.")
        raise