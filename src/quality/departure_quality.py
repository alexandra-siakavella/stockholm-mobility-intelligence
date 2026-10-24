
"""Run data-quality checks on departure observations."""

import os

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


DB_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER", "mobility_user"),
    password=os.getenv("DB_PASSWORD", "mobility_password"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "mobility"),
)

CRITICAL_CHECKS = {
    "missing_journey_id",
    "missing_scheduled",
    "missing_expected",
}


QUERIES = {
    "total_observations": """
        SELECT COUNT(*) FROM departure_observations;
    """,
    "missing_journey_id": """
        SELECT COUNT(*) FROM departure_observations
        WHERE journey_id IS NULL;
    """,
    "missing_scheduled": """
        SELECT COUNT(*) FROM departure_observations
        WHERE scheduled IS NULL;
    """,
    "missing_expected": """
        SELECT COUNT(*) FROM departure_observations
        WHERE expected IS NULL;
    """,
    "negative_delays": """
        SELECT COUNT(*) FROM departure_observations
        WHERE scheduled IS NOT NULL
          AND expected IS NOT NULL
          AND expected < scheduled;
    """,
    "distinct_sites": """
        SELECT COUNT(DISTINCT site_id)
        FROM departure_observations;
    """,
    "distinct_lines": """
        SELECT COUNT(DISTINCT line_designation)
        FROM departure_observations;
    """,
    "earliest_observation": """
        SELECT MIN(observed_at) FROM departure_observations;
    """,
    "latest_observation": """
        SELECT MAX(observed_at) FROM departure_observations;
    """,
}


def run_quality_checks() -> bool:
    """Report data quality and return whether critical checks pass."""

    engine = create_engine(DB_URL)

    try:
        results = {}

        with engine.connect() as connection:
            for name, query in QUERIES.items():
                results[name] = connection.execute(
                    text(query)
                ).scalar_one()

        print("Departure data-quality report")
        print("=" * 40)

        for name, value in results.items():
            print(f"{name}: {value}")

        failures = [
            name
            for name in CRITICAL_CHECKS
            if results[name] > 0
        ]

        if failures:
            print(f"\nFAILED critical checks: {', '.join(failures)}")
            return False

        print("\nCritical data-quality checks passed.")
        return True

    finally:
        engine.dispose()


if __name__ == "__main__":
    if not run_quality_checks():
        raise SystemExit(1)
