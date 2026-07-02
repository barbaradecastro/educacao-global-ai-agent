import argparse
from pathlib import Path
from typing import Any

import pandas as pd

from .charts import create_ranking_bar_chart, create_time_series_chart
from .clean_data import clean_education_data
from .comparisons import compare_countries
from .config import (
    COUNTRY_COMPARISON_FILE,
    DEFAULT_COUNTRIES,
    DEFAULT_END_YEAR,
    DEFAULT_INDICATORS,
    DEFAULT_START_YEAR,
    EDUCATION_METRICS_FILE,
    FINAL_ANALYSIS_CSV,
    FINAL_ANALYSIS_JSON,
    RANKINGS_FILE,
    REPORT_JSON_FILE,
    REPORT_MD_FILE,
    create_required_directories,
)
from .exporters import export_dataframe_to_csv, export_markdown, export_to_json
from .indicators import filter_indicators
from .load_data import load_edstats_data
from .metrics import calculate_metrics
from .openai_client import generate_executive_analysis
from .rankings import rank_by_final_value
from .report_generator import build_markdown_report, build_structured_report
from .transformations import transform_to_long_format
from .utils import (
    setup_logger,
    validate_countries,
    validate_indicators,
    validate_year_range,
)


logger = setup_logger(__name__)

SKIP_OPENAI_ANALYSIS = (
    "Análise OpenAI não executada porque a opção skip-openai foi ativada."
)


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Execute the Global Education AI Agent pipeline."
    )

    parser.add_argument(
        "--countries",
        nargs="+",
        default=DEFAULT_COUNTRIES,
        help="Country codes to analyze.",
    )
    parser.add_argument(
        "--indicators",
        nargs="+",
        default=DEFAULT_INDICATORS,
        help="Education indicator codes to analyze.",
    )
    parser.add_argument(
        "--start-year",
        type=int,
        default=DEFAULT_START_YEAR,
        help="Initial year for analysis.",
    )
    parser.add_argument(
        "--end-year",
        type=int,
        default=DEFAULT_END_YEAR,
        help="Final year for analysis.",
    )
    parser.add_argument(
        "--skip-openai",
        action="store_true",
        help="Skip OpenAI executive analysis generation.",
    )

    return parser


def build_openai_payload(
    metrics_df: pd.DataFrame,
    rankings_df: pd.DataFrame,
    comparisons_df: pd.DataFrame,
    chart_paths: list[Path],
) -> dict[str, Any]:
    """Build the analytical payload sent to OpenAI."""
    if not isinstance(metrics_df, pd.DataFrame):
        raise TypeError("metrics_df must be a pandas DataFrame.")

    if not isinstance(rankings_df, pd.DataFrame):
        raise TypeError("rankings_df must be a pandas DataFrame.")

    if not isinstance(comparisons_df, pd.DataFrame):
        raise TypeError("comparisons_df must be a pandas DataFrame.")

    if not isinstance(chart_paths, list):
        raise TypeError("chart_paths must be a list.")

    return {
        "metrics": metrics_df.copy().head(20).to_dict(orient="records"),
        "rankings": rankings_df.copy().head(20).to_dict(orient="records"),
        "comparisons": comparisons_df.copy().head(20).to_dict(orient="records"),
        "charts": [str(path) for path in chart_paths],
    }


def run_pipeline(
    countries: list[str],
    indicators: list[str],
    start_year: int,
    end_year: int,
    skip_openai: bool = False,
) -> dict[str, object]:
    """Run the full Global Education AI Agent pipeline."""
    logger.info("Starting full education analysis pipeline.")

    try:
        logger.info(
            "Pipeline parameters: countries=%s, indicators=%s, start_year=%s, "
            "end_year=%s, skip_openai=%s",
            countries,
            indicators,
            start_year,
            end_year,
            skip_openai,
        )

        validate_countries(countries)
        validate_indicators(indicators)
        validate_year_range(start_year, end_year)

        create_required_directories()

        datasets = load_edstats_data()
        raw_df = datasets["data"]

        cleaned_df = clean_education_data(raw_df)

        long_df = transform_to_long_format(
            cleaned_df,
            start_year=start_year,
            end_year=end_year,
        )

        filtered_df = filter_indicators(long_df, indicators)

        metrics_df = calculate_metrics(filtered_df)

        rankings_df = rank_by_final_value(metrics_df)

        comparisons_df = compare_countries(
            metrics_df,
            countries=countries,
            indicator_code=indicators[0] if indicators else None,
        )

        ranking_chart_path = create_ranking_bar_chart(
            rankings_df,
            title="Ranking por Valor Final",
            filename="ranking_final_value.png",
        )

        normalized_countries = [country.strip().upper() for country in countries]
        normalized_first_indicator = indicators[0].strip().upper() if indicators else None

        time_series_df = filtered_df[
            filtered_df["country_code"]
            .astype(str)
            .str.strip()
            .str.upper()
            .isin(normalized_countries)
        ].copy()

        if normalized_first_indicator:
            time_series_df = time_series_df[
                time_series_df["indicator_code"]
                .astype(str)
                .str.strip()
                .str.upper()
                .eq(normalized_first_indicator)
            ].copy()

        time_series_chart_path = create_time_series_chart(
            time_series_df,
            title="Evolução Histórica por País",
            filename="historical_evolution.png",
        )

        chart_paths = [ranking_chart_path, time_series_chart_path]

        metrics_path = export_dataframe_to_csv(metrics_df, EDUCATION_METRICS_FILE)
        final_analysis_csv_path = export_dataframe_to_csv(filtered_df, FINAL_ANALYSIS_CSV)
        rankings_path = export_dataframe_to_csv(rankings_df, RANKINGS_FILE)
        comparisons_path = export_dataframe_to_csv(
            comparisons_df,
            COUNTRY_COMPARISON_FILE,
        )

        payload = build_openai_payload(
            metrics_df=metrics_df,
            rankings_df=rankings_df,
            comparisons_df=comparisons_df,
            chart_paths=chart_paths,
        )

        if skip_openai:
            openai_analysis = SKIP_OPENAI_ANALYSIS
        else:
            openai_analysis = generate_executive_analysis(payload)

        markdown_report = build_markdown_report(
            metrics_df=metrics_df,
            rankings_df=rankings_df,
            comparisons_df=comparisons_df,
            openai_analysis=openai_analysis,
        )

        structured_report = build_structured_report(
            metrics_df=metrics_df,
            rankings_df=rankings_df,
            comparisons_df=comparisons_df,
            openai_analysis=openai_analysis,
        )

        report_md_path = export_markdown(markdown_report, REPORT_MD_FILE)
        report_json_path = export_to_json(structured_report, REPORT_JSON_FILE)

        final_analysis_payload = {
            "parameters": {
                "countries": countries,
                "indicators": indicators,
                "start_year": start_year,
                "end_year": end_year,
                "skip_openai": skip_openai,
            },
            "openai_payload": payload,
            "structured_report": structured_report,
            "outputs": {
                "metrics_csv": str(metrics_path),
                "final_analysis_csv": str(final_analysis_csv_path),
                "rankings_csv": str(rankings_path),
                "country_comparison_csv": str(comparisons_path),
                "report_md": str(report_md_path),
                "report_json": str(report_json_path),
                "charts": [str(path) for path in chart_paths],
            },
        }

        final_analysis_json_path = export_to_json(
            final_analysis_payload,
            FINAL_ANALYSIS_JSON,
        )

        status: dict[str, object] = {
            "success": True,
            "countries": countries,
            "indicators": indicators,
            "start_year": start_year,
            "end_year": end_year,
            "skip_openai": skip_openai,
            "outputs": {
                "metrics_csv": str(metrics_path),
                "final_analysis_csv": str(final_analysis_csv_path),
                "final_analysis_json": str(final_analysis_json_path),
                "rankings_csv": str(rankings_path),
                "country_comparison_csv": str(comparisons_path),
                "report_md": str(report_md_path),
                "report_json": str(report_json_path),
                "charts": [str(path) for path in chart_paths],
            },
        }

        logger.info("Pipeline completed successfully.")
        return status

    except TypeError:
        logger.exception("Invalid input type during pipeline execution.")
        raise
    except ValueError:
        logger.exception("Invalid value during pipeline execution.")
        raise
    except KeyError:
        logger.exception("Missing expected key or column during pipeline execution.")
        raise
    except FileNotFoundError:
        logger.exception("Required file not found during pipeline execution.")
        raise
    except OSError:
        logger.exception("File system error during pipeline execution.")
        raise
    except Exception:
        logger.exception("Unexpected error during pipeline execution.")
        raise


def main() -> int:
    """Execute the pipeline from command-line arguments."""
    parser = build_argument_parser()
    args = parser.parse_args()

    try:
        run_pipeline(
            countries=args.countries,
            indicators=args.indicators,
            start_year=args.start_year,
            end_year=args.end_year,
            skip_openai=args.skip_openai,
        )

        logger.info("Execution finished successfully.")
        return 0

    except Exception:
        logger.exception("Execution failed.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())