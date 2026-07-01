import logging
from datetime import datetime
from pathlib import Path


def setup_logger(
    name: str = "educacao_global_ai_agent",
    level: int = logging.INFO,
) -> logging.Logger:
    """Create or retrieve a configured logger without duplicating handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    logger.propagate = False
    return logger


def validate_year_range(start_year: int, end_year: int) -> None:
    """Validate that the year range is made of positive integers and is ordered."""
    if not isinstance(start_year, int):
        raise TypeError("start_year must be an integer.")

    if not isinstance(end_year, int):
        raise TypeError("end_year must be an integer.")

    if start_year <= 0:
        raise ValueError("start_year must be a positive integer.")

    if end_year <= 0:
        raise ValueError("end_year must be a positive integer.")

    if start_year > end_year:
        raise ValueError("start_year must be less than or equal to end_year.")


def validate_countries(countries: list[str]) -> None:
    """Validate a non-empty list of three-character country codes."""
    if not isinstance(countries, list):
        raise TypeError("countries must be a list of strings.")

    if not countries:
        raise ValueError("countries cannot be empty.")

    for country in countries:
        if not isinstance(country, str):
            raise TypeError("all country codes must be strings.")

        if len(country.strip()) != 3:
            raise ValueError(
                f"invalid country code '{country}'. Country codes must have 3 characters."
            )


def validate_indicators(indicators: list[str]) -> None:
    """Validate a non-empty list of indicator codes."""
    if not isinstance(indicators, list):
        raise TypeError("indicators must be a list of strings.")

    if not indicators:
        raise ValueError("indicators cannot be empty.")

    for indicator in indicators:
        if not isinstance(indicator, str):
            raise TypeError("all indicators must be strings.")

        if not indicator.strip():
            raise ValueError("indicator codes cannot be empty.")


def safe_numeric(value: object, default: float | None = None) -> float | None:
    """Safely convert a value to float, returning default when conversion fails."""
    if value is None:
        return default

    if isinstance(value, str) and not value.strip():
        return default

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def save_execution_log(message: str, log_file: Path) -> None:
    """Append a timestamped execution message to a log file."""
    if not isinstance(message, str):
        raise TypeError("message must be a string.")

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().isoformat(timespec="seconds")
    log_entry = f"{timestamp} | {message}\n"

    with log_path.open("a", encoding="utf-8") as file:
        file.write(log_entry)