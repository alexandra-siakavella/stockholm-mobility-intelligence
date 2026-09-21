"""
Train and save the production XGBoost delay prediction model.
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor


DATA_DIR = Path("data/processed/ml")
MODEL_DIR = Path("data/models")

MODEL_PATH = MODEL_DIR / "delay_xgboost.joblib"
PREPROCESSOR_PATH = MODEL_DIR / "delay_preprocessor.joblib"
METRICS_PATH = MODEL_DIR / "delay_model_metrics.csv"

FEATURES = [
    "site_id",
    "line_designation",
    "transport_mode",
    "destination",
    "direction",
    "minutes_until_departure",
    "observation_hour",
    "observation_day_of_week",
    "is_peak_hour",
]

CATEGORICAL_FEATURES = [
    "line_designation",
    "transport_mode",
    "destination",
    "direction",
]

NUMERIC_FEATURES = [
    "site_id",
    "minutes_until_departure",
    "observation_hour",
    "observation_day_of_week",
    "is_peak_hour",
]


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load training and validation datasets."""

    train = pd.read_parquet(
        DATA_DIR / "train.parquet"
    )

    validation = pd.read_parquet(
        DATA_DIR / "validation.parquet"
    )

    return train, validation


def build_preprocessor() -> ColumnTransformer:
    """Build the feature preprocessing pipeline."""

    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                CATEGORICAL_FEATURES,
            ),
            (
                "numeric",
                "passthrough",
                NUMERIC_FEATURES,
            ),
        ]
    )


def calculate_metrics(
    actual: pd.Series,
    predictions,
) -> dict[str, float]:
    """Calculate regression metrics."""

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
    """Train and save the model and preprocessing pipeline."""

    print("Loading training data...")

    train, validation = load_data()

    X_train = train[FEATURES]
    y_train = train["delay_seconds"]

    X_validation = validation[FEATURES]
    y_validation = validation["delay_seconds"]

    print(
        f"Training rows: {len(train)}"
    )

    print(
        f"Validation rows: {len(validation)}"
    )

    print("Building preprocessing pipeline...")

    preprocessor = build_preprocessor()

    X_train_encoded = preprocessor.fit_transform(
        X_train
    )

    X_validation_encoded = preprocessor.transform(
        X_validation
    )

    print("Training XGBoost model...")

    model = XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=42,
    )

    model.fit(
        X_train_encoded,
        y_train,
    )

    validation_predictions = model.predict(
        X_validation_encoded
    )

    metrics = calculate_metrics(
        y_validation,
        validation_predictions,
    )

    print("\nValidation metrics:")

    for metric, value in metrics.items():
        print(
            f"{metric}: {value:.2f}"
        )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    joblib.dump(
        preprocessor,
        PREPROCESSOR_PATH,
    )

    metrics_df = pd.DataFrame(
        [metrics]
    )

    metrics_df.to_csv(
        METRICS_PATH,
        index=False,
    )

    print("\nSaved model:")
    print(MODEL_PATH)

    print("\nSaved preprocessor:")
    print(PREPROCESSOR_PATH)

    print("\nSaved metrics:")
    print(METRICS_PATH)


if __name__ == "__main__":
    main()
    