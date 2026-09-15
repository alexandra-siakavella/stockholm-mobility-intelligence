"""
Transform departure observations into analytics-ready Silver data.
"""

from datetime import datetime
from typing import Any


def calculate_delay_seconds(
    scheduled: datetime | None,
    expected: datetime | None,
) -> float | None:
    """Calculate departure delay in seconds."""

    if scheduled is None or expected is None:
        return None

    return (
        expected - scheduled
    ).total_seconds()


def transform_departure(
    departure: dict[str, Any],
) -> dict[str, Any]:
    """Add analytics-ready fields to a departure observation."""

    scheduled = departure.get("scheduled")
    expected = departure.get("expected")

    transformed = departure.copy()

    transformed["delay_seconds"] = calculate_delay_seconds(
        scheduled,
        expected,
    )

    transformed["is_cancelled"] = (
        departure.get("journey_state")
        == "CANCELLED"
    )

    return transformed
    