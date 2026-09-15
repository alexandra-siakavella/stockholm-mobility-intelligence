"""
Load validated Silver transport-site data into PostgreSQL.
"""

import json
from pathlib import Path

import psycopg2

from src.models.site import Site


SILVER_FILE = Path("data/processed/sl/sites.json")


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "mobility",
    "user": "mobility_user",
    "password": "mobility_password",
}


def load_silver_sites() -> list[Site]:
    """Load and validate Silver records."""

    with SILVER_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        records = json.load(file)

    return [
        Site(**record)
        for record in records
    ]


def insert_sites(sites: list[Site]) -> int:
    """Insert validated sites into PostgreSQL."""

    connection = psycopg2.connect(
        **DB_CONFIG
    )

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.executemany(
                    """
                    INSERT INTO transport_sites (
                        site_id,
                        gid,
                        site_name,
                        note,
                        latitude,
                        longitude,
                        valid_from
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (site_id)
                    DO UPDATE SET
                        gid = EXCLUDED.gid,
                        site_name = EXCLUDED.site_name,
                        note = EXCLUDED.note,
                        latitude = EXCLUDED.latitude,
                        longitude = EXCLUDED.longitude,
                        valid_from = EXCLUDED.valid_from
                    """,
                    [
                        (
                            site.site_id,
                            site.gid,
                            site.site_name,
                            site.note,
                            site.latitude,
                            site.longitude,
                            site.valid_from,
                        )
                        for site in sites
                    ],
                )

        return len(sites)

    finally:
        connection.close()


if __name__ == "__main__":
    sites = load_silver_sites()

    loaded_count = insert_sites(sites)

    print(
        f"Validated Silver records: {len(sites)}"
    )

    print(
        f"Records loaded into PostgreSQL: "
        f"{loaded_count}"
    )