"""
Collect departure observations from the configured SL sites.
"""

import time

from src.config import SL_SITE_IDS
from src.database.load_departures import insert_departures
from src.ingestion.departures import (
    get_departures,
    save_departures,
)


def collect_departures() -> list[dict]:
    """Collect departures from all configured SL sites."""

    all_departures = []

    for site_id in SL_SITE_IDS:
        departures = get_departures(site_id)

        if not departures:
            print(
                f"Site {site_id}: "
                "0 departures. Retrying..."
            )

            time.sleep(2)

            departures = get_departures(site_id)

        if not departures:
            print(
                f"WARNING: Site {site_id} "
                "returned 0 departures after retry."
            )

        else:
            print(
                f"Site {site_id}: "
                f"{len(departures)} departures."
            )

        all_departures.extend(departures)

    return all_departures


def main() -> None:
    """Run one complete departure collection cycle."""

    print(
        "Starting departure collection..."
    )

    departures = collect_departures()

    output_file = save_departures(
        departures
    )

    loaded_count = insert_departures(
        departures
    )

    print(
        f"\nTotal departures: "
        f"{len(departures)}"
    )

    print(
        f"Raw data saved to: "
        f"{output_file}"
    )

    print(
        f"New observations loaded into "
        f"PostgreSQL: {loaded_count}"
    )

    print(
        "Departure collection completed."
    )


if __name__ == "__main__":
    main()
