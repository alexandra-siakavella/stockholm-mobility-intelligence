from src.quality.site_validation import validate_sites


def test_valid_site_has_no_errors():
    sites = [
        {
            "id": 1,
            "name": "Test Station",
            "lat": 59.33,
            "lon": 18.06,
        }
    ]

    errors = validate_sites(sites)

    assert errors == []


def test_missing_coordinates_are_flagged():
    sites = [
        {
            "id": 2,
            "name": "Invalid Station",
        }
    ]

    errors = validate_sites(sites)

    assert len(errors) == 1
    assert errors[0]["reason"] == "Missing fields: ['lat', 'lon']"


def test_invalid_latitude_is_flagged():
    sites = [
        {
            "id": 3,
            "name": "Invalid Latitude",
            "lat": 120,
            "lon": 18.06,
        }
    ]

    errors = validate_sites(sites)

    assert len(errors) == 1
    assert errors[0]["reason"] == "Latitude outside valid range"


def test_invalid_longitude_is_flagged():
    sites = [
        {
            "id": 4,
            "name": "Invalid Longitude",
            "lat": 59.33,
            "lon": 200,
        }
    ]

    errors = validate_sites(sites)

    assert len(errors) == 1
    assert errors[0]["reason"] == "Longitude outside valid range"