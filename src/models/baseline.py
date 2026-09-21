"""
Train and evaluate a mean-delay baseline model.
"""

from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)


DATA_DIR = Path("data/processed/ml")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load train, validation, and test datasets."""

    train = pd.read_parquet(
        DATA_DIR / "train.parquet"
    )

    validation = pd.read_parquet(
        DATA_DIR / "validation.parquet"
    )

    test = pd.read_parquet(
        DATA_DIR / "test.parquet"
    )

    return train, validation, test


def evaluate(
    actual: pd.Series,
    prediction: float,
) -> dict[str, float]:
    """Calculate regression metrics."""

    predictions = [prediction] * len(actual)

    mae = mean_absolute_error(
        actual,
        predictions,
    )

    rmse = mean_squared_error(
        actual,
        predictions,
    ) ** 0.5

    return {
        "MAE": mae,
        "RMSE": rmse,
    }


def main() -> None:
    """Run the baseline model."""

    train, validation, test = load_data()

    baseline_prediction = train[
        "delay_seconds"
    ].mean()

    print(
        f"Baseline prediction: "
        f"{baseline_prediction:.2f} seconds"
    )

    validation_metrics = evaluate(
        validation["delay_seconds"],
        baseline_prediction,
    )

    test_metrics = evaluate(
        test["delay_seconds"],
        baseline_prediction,
    )

    print("\nValidation metrics:")
    for metric, value in validation_metrics.items():
        print(f"{metric}: {value:.2f}")

    print("\nTest metrics:")
    for metric, value in test_metrics.items():
        print(f"{metric}: {value:.2f}")


if __name__ == "__main__":
    main()
    