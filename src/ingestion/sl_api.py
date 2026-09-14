"""
Client for retrieving public transport data from the SL Transport API.

The API is provided through Trafiklab and returns JSON data.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from src.quality.site_validation import validate_sites

BASE_URL = "https://transport.integration.sl.se/v1"

RAW_DATA_DIR = Path("data/raw/sl")


def get_sites() -> list[dict[str, Any]]:
    """Retrieve all SL transport sites."""
    response = requests.get(
        f"{BASE_URL}/sites",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def save_raw_data(data: list[dict[str, Any]]) -> tuple[Path, Path]:
    """Save raw API response and ingestion metadata."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_file = RAW_DATA_DIR / "sites.json"
    metadata_file = RAW_DATA_DIR / "metadata.json"

    ingestion_timestamp = datetime.now(timezone.utc).isoformat()

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    metadata = {
        "source": "SL Transport API",
        "endpoint": f"{BASE_URL}/sites",
        "ingested_at": ingestion_timestamp,
        "record_count": len(data),
        "output_file": str(output_file),
    }

    with metadata_file.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=2)

    return output_file, metadata_file


if __name__ == "__main__":
    sites = get_sites()

    validate_sites(sites)

    output_file, metadata_file = save_raw_data(sites)

    print(f"Retrieved {len(sites)} transport sites.")
    print(f"Raw data saved to: {output_file}")
    print(f"Metadata saved to: {metadata_file}")