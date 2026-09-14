"""
Transform validated SL transport site data into the Silver layer.
"""

import json
from pathlib import Path
from typing import Any


RAW_FILE = Path("data/raw/sl/sites.json")
QUARANTINE_FILE = Path(
    "data/quarantine/sl/invalid_sites.json"
)
SILVER_DIR = Path("data/processed/sl")


def load_raw_sites() -> list[dict[str, Any]]:
    """Load the complete Bronze dataset."""

    with RAW_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def load_quarantine() -> set[int]:
    """Load IDs of records that failed validation."""

    with QUARANTINE_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        invalid_sites = json.load(file)

    return {
        record["site"]["id"]
        for record in invalid_sites
    }


def transform_sites(
    sites: list[dict[str, Any]],
    invalid_ids: set[int],
) -> list[dict[str, Any]]:
    """Transform valid Bronze records into Silver records."""

    silver_sites = []

    for site in sites:
        if site["id"] in invalid_ids:
            continue

        silver_sites.append(
            {
                "site_id": site["id"],
                "gid": site["gid"],
                "site_name": site["name"],
                "note": site.get("note"),
                "latitude": site["lat"],
                "longitude": site["lon"],
                "valid_from": site["valid"]["from"],
            }
        )

    return silver_sites


def save_silver_data(
    sites: list[dict[str, Any]],
) -> Path:
    """Save the transformed Silver dataset."""

    SILVER_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = SILVER_DIR / "sites.json"

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            sites,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return output_file


if __name__ == "__main__":
    sites = load_raw_sites()

    invalid_ids = load_quarantine()

    silver_sites = transform_sites(
        sites,
        invalid_ids,
    )

    output_file = save_silver_data(
        silver_sites
    )

    print(
        f"Bronze records: {len(sites)}"
    )

    print(
        f"Quarantined records: {len(invalid_ids)}"
    )

    print(
        f"Silver records: {len(silver_sites)}"
    )

    print(
        f"Silver data saved to: {output_file}"
    )