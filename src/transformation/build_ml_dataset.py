"""
Build a machine-learning dataset from PostgreSQL departure features.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


DB_URL = (
    "postgresql+psycopg2://"
    f"{os.getenv('DB_USER', 'mobility_user')}:"
    f"{os.getenv('DB_PASSWORD', 'mobility_password')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'mobility')}"
)
OUTPUT_PATH = Path("data/processed/departure_ml_dataset.parquet")


def load_features() -> pd.DataFrame:
    """Load ML features from PostgreSQL."""
    engine = create_engine(DB_URL)

    query = """
        SELECT *
        FROM departure_ml_features
        ORDER BY observed_at, observation_id
    """

    return pd.read_sql(query, engine)


def prepare_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare features and target for machine learning."""

    df = df.copy()

    df["observed_at"] = pd.to_datetime(df["observed_at"], utc=True)
    df["scheduled"] = pd.to_datetime(df["scheduled"], utc=True)

    categorical_columns = [
        "line_designation",
        "transport_mode",
        "destination",
        "direction",
    ]

    for column in categorical_columns:
        df[column] = df[column].fillna("UNKNOWN")

    df = df.sort_values(
        ["observed_at", "observation_id"]
    ).reset_index(drop=True)

    return df


def save_dataset(df: pd.DataFrame) -> None:
    """Save the prepared dataset as Parquet."""

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_parquet(
        OUTPUT_PATH,
        index=False,
    )

    print(f"Saved dataset to: {OUTPUT_PATH}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")


def main() -> None:
    """Build the machine-learning dataset."""

    print("Loading departure features...")

    df = load_features()

    print(f"Loaded rows: {len(df)}")

    df = prepare_dataset(df)

    save_dataset(df)


if __name__ == "__main__":
    main()
    