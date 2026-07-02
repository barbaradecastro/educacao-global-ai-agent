import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
OUTPUT_DATA_DIR: Path = DATA_DIR / "output"

REPORTS_DIR: Path = PROJECT_ROOT / "reports"
N8N_DIR: Path = PROJECT_ROOT / "n8n"
SKILLS_DIR: Path = PROJECT_ROOT / "skills"
CHARTS_DIR: Path = OUTPUT_DATA_DIR / "charts"


EDSTATS_DATA_FILE: Path = RAW_DATA_DIR / "EdStatsData.csv"
EDSTATS_COUNTRY_FILE: Path = RAW_DATA_DIR / "EdStatsCountry.csv"
EDSTATS_SERIES_FILE: Path = RAW_DATA_DIR / "EdStatsSeries.csv"
EDSTATS_FOOTNOTE_FILE: Path = RAW_DATA_DIR / "EdStatsFootNote.csv"


EDUCATION_CLEAN_FILE: Path = PROCESSED_DATA_DIR / "education_clean.csv"
EDUCATION_FILTERED_FILE: Path = PROCESSED_DATA_DIR / "education_filtered.csv"
EDUCATION_METRICS_FILE: Path = OUTPUT_DATA_DIR / "education_metrics.csv"
FINAL_ANALYSIS_CSV: Path = OUTPUT_DATA_DIR / "final_analysis.csv"
FINAL_ANALYSIS_JSON: Path = OUTPUT_DATA_DIR / "final_analysis.json"
RANKINGS_FILE: Path = OUTPUT_DATA_DIR / "rankings.csv"
COUNTRY_COMPARISON_FILE: Path = OUTPUT_DATA_DIR / "country_comparison.csv"

REPORT_MD_FILE: Path = REPORTS_DIR / "report.md"
REPORT_JSON_FILE: Path = REPORTS_DIR / "report.json"
REPORT_PDF_FILE: Path = REPORTS_DIR / "report.pdf"


DEFAULT_COUNTRIES: list[str] = ["BRA", "CHL", "ARG", "USA", "FIN"]
DEFAULT_INDICATORS: list[str] = ["SE.XPD.TOTL.GD.ZS", "SE.ADT.LITR.ZS"]
DEFAULT_START_YEAR: int = 2000
DEFAULT_END_YEAR: int = 2020


OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


REQUIRED_DIRECTORIES: list[Path] = [
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    OUTPUT_DATA_DIR,
    REPORTS_DIR,
    N8N_DIR,
    SKILLS_DIR,
    CHARTS_DIR,
]

RAW_EDSTATS_FILES: list[Path] = [
    EDSTATS_DATA_FILE,
    EDSTATS_COUNTRY_FILE,
    EDSTATS_SERIES_FILE,
    EDSTATS_FOOTNOTE_FILE,
]

OUTPUT_FILES: list[Path] = [
    EDUCATION_CLEAN_FILE,
    EDUCATION_FILTERED_FILE,
    EDUCATION_METRICS_FILE,
    FINAL_ANALYSIS_CSV,
    FINAL_ANALYSIS_JSON,
    RANKINGS_FILE,
    COUNTRY_COMPARISON_FILE,
    REPORT_MD_FILE,
    REPORT_JSON_FILE,
    REPORT_PDF_FILE,
]


def create_required_directories() -> None:
    """Create all directories required by the project if they do not exist."""
    for directory in REQUIRED_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


def validate_raw_files() -> list[Path]:
    """
    Validate the presence of required raw EdStats files.

    Returns:
        A list of missing raw EdStats file paths.
    """
    return [file_path for file_path in RAW_EDSTATS_FILES if not file_path.exists()]