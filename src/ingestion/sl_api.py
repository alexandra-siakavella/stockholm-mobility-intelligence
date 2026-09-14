"""
Client for retrieving public transport data from the SL Transport API.

Pipeline:

SL Transport API
        ↓
    Validation
        ↓
 ┌──────┴──────┐
 ↓             ↓
Valid        Invalid
 ↓             ↓
Bronze      Quarantine
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

from src.quality.site_validation import validate_sites


BASE_URL = "https://transport.integration.sl.se/v1"

RAW_DATA_DIR = Path("data/raw/sl")
QUARANTINE_DIR = Path("data/quarantine/sl")


def get_sites() -> list[dict[str, Any]]:
    """Retrieve all SL transport sites from the API."""

    response = requests.get(
        f"{BASE_URL}/sites",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def save_raw_data(
    data: list[dict[str, Any]],
) -> tuple[Path, Path]:
    """Save the raw API response and ingestion metadata."""

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = RAW_DATA_DIR / "sites.json"
    metadata_file = RAW_DATA_DIR / "metadata.json"

    ingestion_timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    # Save raw API response.
    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    # Create ingestion metadata.
    metadata = {
        "source": "SL Transport API",
        "endpoint": f"{BASE_URL}/sites",
        "ingested_at": ingestion_timestamp,
        "record_count": len(data),
        "output_file": str(output_file),
    }

    with metadata_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return output_file, metadata_file


def save_quarantine_data(
    invalid_sites: list[dict[str, Any]],
) -> Path:
    """Save records that failed data-quality validation."""

    QUARANTINE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        QUARANTINE_DIR / "invalid_sites.json"
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            invalid_sites,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return output_file


if __name__ == "__main__":
    # 1. Extract data from the SL API.
    sites = get_sites()

    # 2. Validate the incoming data.
    invalid_sites = validate_sites(sites)

    # 3. Preserve the complete API response in Bronze.
    output_file, metadata_file = save_raw_data(sites)

    # 4. Save invalid records to the quarantine layer.
    quarantine_file = save_quarantine_data(
        invalid_sites
    )

    # 5. Report pipeline results.
    print(
        f"Retrieved {len(sites)} transport sites."
    )

    print(
        f"Data-quality issues detected: "
        f"{len(invalid_sites)}"
    )

    print(
        f"Raw data saved to: {output_file}"
    )

    print(
        f"Metadata saved to: {metadata_file}"
    )

    print(
        f"Quarantined data saved to: "
        f"{quarantine_file}"
    )