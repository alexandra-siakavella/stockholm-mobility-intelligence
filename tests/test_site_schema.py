import pytest
from pydantic import ValidationError

from src.models.site import Site


def test_valid_site_is_accepted():
    site = Site(
        site_id=102,
        gid=9091001000000102,
        site_name="Styrsvik",
        note="Runmarö",
        latitude=59.2802666088178,
        longitude=18.7313783519481,
        valid_from="2012-06-23T00:00:00",
    )

    assert site.site_id == 102
    assert site.latitude == 59.2802666088178
    assert site.longitude == 18.7313783519481


def test_invalid_site_id_is_rejected():
    with pytest.raises(ValidationError):
        Site(
            site_id="invalid",
            gid=9091001000000102,
            site_name="Styrsvik",
            latitude=59.2802666088178,
            longitude=18.7313783519481,
            valid_from="2012-06-23T00:00:00",
        )


def test_missing_site_name_is_rejected():
    with pytest.raises(ValidationError):
        Site(
            site_id=102,
            gid=9091001000000102,
            latitude=59.2802666088178,
            longitude=18.7313783519481,
            valid_from="2012-06-23T00:00:00",
        )