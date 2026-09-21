"""
Create chronological train, validation, and test splits.
"""

from pathlib import Path

import pandas as pd


INPUT_PATH = Path(
    "data/processed/departure_ml_dataset.parquet"
)

OUTPUT_DIR = Path(
    "data/processed/ml"
)


def create_splits(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Create chronological splits without splitting journeys."""

    df = df.sort_values(
        ["observed_at", "journey_id", "observation_id"]
    ).reset_index(drop=True)

    n = len(df)

    train_end = int(n * 0.70)
    validation_end = int(n * 0.85)

    train_cutoff = df.loc[
        train_end,
        "observed_at",
    ]

    validation_cutoff = df.loc[
        validation_end,
        "observed_at",
    ]

    train = df[
        df["observed_at"] < train_cutoff
    ].copy()

    validation = df[
        (df["observed_at"] >= train_cutoff)
        & (df["observed_at"] < validation_cutoff)
    ].copy()

    test = df[
        df["observed_at"] >= validation_cutoff
    ].copy()

    return train, validation, test


def save_splits(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    test: pd.DataFrame,
) -> None:
    """Save the three chronological datasets."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    train.to_parquet(
        OUTPUT_DIR / "train.parquet",
        index=False,
    )

    validation.to_parquet(
        OUTPUT_DIR / "validation.parquet",
        index=False,
    )

    test.to_parquet(
        OUTPUT_DIR / "test.parquet",
        index=False,
    )


def main() -> None:
    """Create and save chronological dataset splits."""

    df = pd.read_parquet(INPUT_PATH)

    train, validation, test = create_splits(df)

    save_splits(
        train,
        validation,
        test,
    )

    print(f"Total rows: {len(df)}")
    print(f"Training rows: {len(train)}")
    print(f"Validation rows: {len(validation)}")
    print(f"Test rows: {len(test)}")

    print("\nTraining period:")
    print(train["observed_at"].min())
    print(train["observed_at"].max())

    print("\nValidation period:")
    print(validation["observed_at"].min())
    print(validation["observed_at"].max())

    print("\nTest period:")
    print(test["observed_at"].min())
    print(test["observed_at"].max())


if __name__ == "__main__":
    main()
    