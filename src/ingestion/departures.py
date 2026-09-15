"""
Collect and persist departure observations from the SL Transport API.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


BASE_URL = "https://transport.integration.sl.se/v1"

RAW_DEPARTURES_DIR = Path("data/raw/departures")


def get_departures(
    site_id: int,
) -> list[dict[str, Any]]:
    """Retrieve current departures for an SL transport site."""

    response = requests.get(
        f"{BASE_URL}/sites/{site_id}/departures",
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    observed_at = datetime.now(
        timezone.utc
    ).isoformat()

    departures = []

    for departure in data.get("departures", []):
        line = departure.get("line", {})
        stop_area = departure.get("stop_area", {})
        stop_point = departure.get("stop_point", {})
        journey = departure.get("journey", {})

        departures.append(
            {
                "site_id": site_id,
                "observed_at": observed_at,
                "destination": departure.get(
                    "destination"
                ),
                "direction_code": departure.get(
                    "direction_code"
                ),
                "direction": departure.get(
                    "direction"
                ),
                "state": departure.get("state"),
                "display": departure.get("display"),
                "scheduled": departure.get(
                    "scheduled"
                ),
                "expected": departure.get(
                    "expected"
                ),
                "journey_id": journey.get("id"),
                "journey_state": journey.get(
                    "state"
                ),
                "stop_area_id": stop_area.get(
                    "id"
                ),
                "stop_area_name": stop_area.get(
                    "name"
                ),
                "stop_point_id": stop_point.get(
                    "id"
                ),
                "stop_point_name": stop_point.get(
                    "name"
                ),
                "line_id": line.get("id"),
                "line_designation": line.get(
                    "designation"
                ),
                "transport_authority_id": line.get(
                    "transport_authority_id"
                ),
                "transport_mode": line.get(
                    "transport_mode"
                ),
                "group_of_lines": line.get(
                    "group_of_lines"
                ),
                "deviations": departure.get(
                    "deviations",
                    [],
                ),
            }
        )

    return departures


def save_departures(
    departures: list[dict[str, Any]],
) -> Path:
    """Save departure observations as a timestamped JSON file."""

    RAW_DEPARTURES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%dT%H%M%SZ")

    output_file = (
        RAW_DEPARTURES_DIR
        / f"departures_{timestamp}.json"
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            departures,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return output_file


if __name__ == "__main__":
    site_ids = [9001, 1002]

    all_departures = []

    for site_id in site_ids:
        departures = get_departures(site_id)

        all_departures.extend(
            departures
        )

        print(
            f"Site {site_id}: "
            f"{len(departures)} departures."
        )

    output_file = save_departures(
        all_departures
    )

    print(
        f"Total departures: "
        f"{len(all_departures)}"
    )

    print(
        f"Saved observations to: "
        f"{output_file}"
    )

    for departure in all_departures[:5]:
        print(departure)