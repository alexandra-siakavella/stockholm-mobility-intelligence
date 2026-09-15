"""
Orchestrate the Stockholm Mobility data pipeline.
"""

from src.database.load_sites import (
    insert_sites,
    load_silver_sites,
)
from src.ingestion.sl_api import (
    get_sites,
    save_quarantine_data,
    save_raw_data,
)
from src.quality.site_validation import validate_sites
from src.transformation.sites import (
    load_quarantine,
    load_raw_sites,
    save_silver_data,
    transform_sites,
)


def run_pipeline() -> None:
    """Run the complete SL transport data pipeline."""

    print("Starting Stockholm Mobility pipeline...")

    # 1. Extract
    sites = get_sites()
    print(f"Retrieved {len(sites)} transport sites.")

    # 2. Validate
    invalid_sites = validate_sites(sites)
    print(
        f"Data-quality issues detected: "
        f"{len(invalid_sites)}"
    )

    # 3. Bronze
    save_raw_data(sites)
    save_quarantine_data(invalid_sites)
    print("Bronze and quarantine layers updated.")

    # 4. Silver
    raw_sites = load_raw_sites()
    invalid_ids = load_quarantine()

    silver_sites = transform_sites(
        raw_sites,
        invalid_ids,
    )

    save_silver_data(silver_sites)

    print(
        f"Silver records created: "
        f"{len(silver_sites)}"
    )

    # 5. PostgreSQL
    validated_sites = load_silver_sites()
    loaded_count = insert_sites(validated_sites)

    print(
        f"Records loaded into PostgreSQL: "
        f"{loaded_count}"
    )

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()