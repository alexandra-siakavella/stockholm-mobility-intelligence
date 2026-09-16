"""
Create chronological train, validation, and test splits.
"""

from pathlib import Path

import pandas as pd


INPUT_PATH = Path("data/processed/departure_ml_dataset.parquet")
OUTPUT_DIR = Path("data/processed/ml")


def create_splits(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split the dataset chronologically into train, validation, and test sets."""

    df = df.sort_values(
        ["observed_at", "observation_id"]
    ).reset_index(drop=True)

    n = len(df)

    train_end = int(n * 0.70)
    validation_end = int(n * 0.85)

    train = df.iloc[:train_end].copy()
    validation = df.iloc[train_end:validation_end].copy()
    test = df.iloc[validation_end:].copy()

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

    print()
    print("Training period:")
    print(train["observed_at"].min())
    print(train["observed_at"].max())

    print()
    print("Validation period:")
    print(validation["observed_at"].min())
    print(validation["observed_at"].max())

    print()
    print("Test period:")
    print(test["observed_at"].min())
    print(test["observed_at"].max())


if __name__ == "__main__":
    main()
    