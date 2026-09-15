"""
Run the complete departure data pipeline.
"""

from src.config import SL_SITE_IDS
from src.database.load_departures import (
    insert_departures,
    load_raw_departures,
)
from src.ingestion.departures import (
    get_departures,
    save_departures,
)


def run_pipeline() -> None:
    """Collect and load departure observations."""

    print("Starting departure pipeline...")

    all_departures = []

    for site_id in SL_SITE_IDS:
        departures = get_departures(site_id)

        all_departures.extend(departures)

        print(
            f"Site {site_id}: "
            f"{len(departures)} departures."
        )

    output_file = save_departures(
        all_departures
    )

    print(
        f"Raw data saved to: "
        f"{output_file}"
    )

    departures = load_raw_departures(
        output_file
    )

    loaded_count = insert_departures(
        departures
    )

    print(
        f"New raw observations: "
        f"{len(departures)}"
    )

    print(
        f"Records loaded into PostgreSQL: "
        f"{loaded_count}"
    )

    print(
        "Departure pipeline completed."
    )


if __name__ == "__main__":
    run_pipeline()
    