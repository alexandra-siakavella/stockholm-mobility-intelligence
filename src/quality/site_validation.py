"""
Data-quality checks for SL transport site data.
"""

from typing import Any


def validate_sites(sites: list[dict[str, Any]]) -> None:
    """
    Validate the structure and basic values of SL transport sites.

    Raises:
        ValueError: If any data-quality rule fails.
    """

    if not sites:
        raise ValueError("No transport sites were returned.")

    required_fields = {"id", "name", "lat", "lon"}

    for index, site in enumerate(sites):
        missing_fields = required_fields - site.keys()

        if missing_fields:
            raise ValueError(
                f"Site at index {index} is missing: {missing_fields}"
            )

        latitude = site["lat"]
        longitude = site["lon"]

        if not isinstance(latitude, (int, float)):
            raise ValueError(
                f"Invalid latitude at index {index}: {latitude}"
            )

        if not isinstance(longitude, (int, float)):
            raise ValueError(
                f"Invalid longitude at index {index}: {longitude}"
            )

        if not -90 <= latitude <= 90:
            raise ValueError(
                f"Latitude outside valid range at index {index}: {latitude}"
            )

        if not -180 <= longitude <= 180:
            raise ValueError(
                f"Longitude outside valid range at index {index}: {longitude}"
            )
