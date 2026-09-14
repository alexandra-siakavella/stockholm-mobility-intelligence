"""
Data-quality checks for SL transport site data.
"""

from typing import Any


def validate_sites(
    sites: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Validate SL transport sites and return invalid records.

    Records with missing or invalid coordinates are flagged rather
    than causing the entire ingestion pipeline to fail.
    """

    invalid_sites = []

    required_fields = {"id", "name", "lat", "lon"}

    for index, site in enumerate(sites):
        missing_fields = required_fields - site.keys()

        if missing_fields:
            invalid_sites.append(
                {
                    "index": index,
                    "site": site,
                    "reason": f"Missing fields: {sorted(missing_fields)}",
                }
            )
            continue

        latitude = site["lat"]
        longitude = site["lon"]

        if not isinstance(latitude, (int, float)):
            invalid_sites.append(
                {
                    "index": index,
                    "site": site,
                    "reason": "Invalid latitude",
                }
            )
            continue

        if not isinstance(longitude, (int, float)):
            invalid_sites.append(
                {
                    "index": index,
                    "site": site,
                    "reason": "Invalid longitude",
                }
            )
            continue

        if not -90 <= latitude <= 90:
            invalid_sites.append(
                {
                    "index": index,
                    "site": site,
                    "reason": "Latitude outside valid range",
                }
            )
            continue

        if not -180 <= longitude <= 180:
            invalid_sites.append(
                {
                    "index": index,
                    "site": site,
                    "reason": "Longitude outside valid range",
                }
            )

    return invalid_sites