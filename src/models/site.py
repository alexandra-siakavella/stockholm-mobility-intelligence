from datetime import datetime

from pydantic import BaseModel


class Site(BaseModel):
    """Schema for a validated SL transport site."""

    site_id: int
    gid: int
    site_name: str
    note: str | None = None
    latitude: float
    longitude: float
    valid_from: datetime