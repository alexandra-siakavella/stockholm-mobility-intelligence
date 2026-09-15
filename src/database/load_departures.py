"""
Load raw departure observations into PostgreSQL.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import psycopg2


RAW_DEPARTURES_DIR = Path("data/raw/departures")


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "mobility",
    "user": "mobility_user",
    "password": "mobility_password",
}


def load_raw_departures(
    file_path: Path,
) -> list[dict[str, Any]]:
    """Load departure observations from one raw file."""

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def parse_timestamp(
    value: str | None,
) -> datetime | None:
    """Parse an ISO timestamp."""

    if value is None:
        return None

    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )


def insert_departures(
    departures: list[dict[str, Any]],
) -> int:
    """Insert departure observations into PostgreSQL."""

    connection = psycopg2.connect(
        **DB_CONFIG
    )

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.executemany(
                    """
                    INSERT INTO departure_observations (
                        site_id,
                        observed_at,
                        journey_id,
                        journey_state,
                        line_id,
                        line_designation,
                        transport_mode,
                        group_of_lines,
                        destination,
                        direction,
                        direction_code,
                        scheduled,
                        expected,
                        state,
                        stop_area_id,
                        stop_area_name,
                        stop_point_id,
                        stop_point_name,
                        display,
                        transport_authority_id,
                        deviations
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s
                    )
                    """,
                    [
                        (
                            departure["site_id"],
                            parse_timestamp(
                                departure["observed_at"]
                            ),
                            departure.get("journey_id"),
                            departure.get("journey_state"),
                            departure.get("line_id"),
                            departure.get(
                                "line_designation"
                            ),
                            departure.get(
                                "transport_mode"
                            ),
                            departure.get(
                                "group_of_lines"
                            ),
                            departure.get(
                                "destination"
                            ),
                            departure.get(
                                "direction"
                            ),
                            departure.get(
                                "direction_code"
                            ),
                            parse_timestamp(
                                departure.get(
                                    "scheduled"
                                )
                            ),
                            parse_timestamp(
                                departure.get(
                                    "expected"
                                )
                            ),
                            departure.get("state"),
                            departure.get(
                                "stop_area_id"
                            ),
                            departure.get(
                                "stop_area_name"
                            ),
                            departure.get(
                                "stop_point_id"
                            ),
                            departure.get(
                                "stop_point_name"
                            ),
                            departure.get("display"),
                            departure.get(
                                "transport_authority_id"
                            ),
                            json.dumps(
                                departure.get(
                                    "deviations",
                                    [],
                                )
                            ),
                        )
                        for departure in departures
                    ],
                )

        return len(departures)

    finally:
        connection.close()


if __name__ == "__main__":
    files = sorted(
        RAW_DEPARTURES_DIR.glob(
            "departures_*.json"
        )
    )

    if not files:
        print("No raw departure files found.")

    else:
        latest_file = files[-1]

        departures = load_raw_departures(
            latest_file
        )

        loaded_count = insert_departures(
            departures
        )

        print(
            f"Loaded file: {latest_file}"
        )

        print(
            f"Raw departure observations: "
            f"{len(departures)}"
        )

        print(
            f"Records loaded into PostgreSQL: "
            f"{loaded_count}"
        )
