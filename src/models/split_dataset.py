"""
Create journey-aware chronological train, validation, and test splits.
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

    journey_times = (
        df.groupby("journey_id")["observed_at"]
        .min()
        .sort_values()
    )

    n_journeys = len(journey_times)

    train_journey_end = int(
        n_journeys * 0.70
    )

    validation_journey_end = int(
        n_journeys * 0.85
    )

    train_journeys = set(
        journey_times.iloc[
            :train_journey_end
        ].index
    )

    validation_journeys = set(
        journey_times.iloc[
            train_journey_end:validation_journey_end
        ].index
    )

    test_journeys = set(
        journey_times.iloc[
            validation_journey_end:
        ].index
    )

    train = df[
        df["journey_id"].isin(
            train_journeys
        )
    ].copy()

    validation = df[
        df["journey_id"].isin(
            validation_journeys
        )
    ].copy()

    test = df[
        df["journey_id"].isin(
            test_journeys
        )
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
    """Create and save journey-aware chronological splits."""

    df = pd.read_parquet(
        INPUT_PATH
    )

    train, validation, test = create_splits(
        df
    )

    save_splits(
        train,
        validation,
        test,
    )

    print(
        f"Total rows: {len(df)}"
    )

    print(
        f"Training rows: {len(train)}"
    )

    print(
        f"Validation rows: {len(validation)}"
    )

    print(
        f"Test rows: {len(test)}"
    )

    print(
        f"\nTraining journeys: "
        f"{train['journey_id'].nunique()}"
    )

    print(
        f"Validation journeys: "
        f"{validation['journey_id'].nunique()}"
    )

    print(
        f"Test journeys: "
        f"{test['journey_id'].nunique()}"
    )

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
    