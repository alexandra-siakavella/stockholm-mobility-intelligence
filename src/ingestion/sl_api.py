"""
Client for retrieving public transport data from the SL Transport API.

The API is provided through Trafiklab and returns JSON data.
"""

from typing import Any

import requests


BASE_URL = "https://transport.integration.sl.se/v1"


def get_sites() -> list[dict[str, Any]]:
    """Retrieve all SL transport sites."""
    response = requests.get(
        f"{BASE_URL}/sites",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    sites = get_sites()

    print(f"Retrieved {len(sites)} transport sites.")
    print(sites[:3])
