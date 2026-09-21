"""
Train and evaluate an XGBoost delay prediction model.
"""

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor


DATA_DIR = Path("data/processed/ml")

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


def build_preprocessor() -> ColumnTransformer:
    """Create preprocessing for categorical and numeric features."""

    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore",
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


def evaluate(
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


def aggregate_feature_importance(
    feature_names,
    importances,
) -> pd.Series:
    """Aggregate one-hot feature importance to original features."""

    feature_importance = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importances,
        }
    )

    def get_original_feature(feature_name: str) -> str:
        """Map encoded feature back to its original feature."""

        if feature_name.startswith("categorical__"):
            encoded_name = feature_name.replace(
                "categorical__",
                "",
                1,
            )

            for column in CATEGORICAL_FEATURES:
                if (
                    encoded_name == column
                    or encoded_name.startswith(
                        f"{column}_"
                    )
                ):
                    return column

        if feature_name.startswith("numeric__"):
            return feature_name.replace(
                "numeric__",
                "",
                1,
            )

        return feature_name

    feature_importance["original_feature"] = (
        feature_importance["feature"]
        .map(get_original_feature)
    )

    return (
        feature_importance
        .groupby("original_feature")["importance"]
        .sum()
        .sort_values(ascending=False)
    )


def main() -> None:
    """Train and evaluate the XGBoost model."""

    train, validation, test = load_data()

    X_train = train[FEATURES]
    y_train = train["delay_seconds"]

    X_validation = validation[FEATURES]
    y_validation = validation["delay_seconds"]

    X_test = test[FEATURES]
    y_test = test["delay_seconds"]

    preprocessor = build_preprocessor()

    X_train_encoded = preprocessor.fit_transform(
        X_train
    )

    X_validation_encoded = preprocessor.transform(
        X_validation
    )

    X_test_encoded = preprocessor.transform(
        X_test
    )

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

    test_predictions = model.predict(
        X_test_encoded
    )

    validation_metrics = evaluate(
        y_validation,
        validation_predictions,
    )

    test_metrics = evaluate(
        y_test,
        test_predictions,
    )

    print("XGBoost validation metrics:")

    for metric, value in validation_metrics.items():
        print(
            f"{metric}: {value:.2f}"
        )

    print("\nXGBoost test metrics:")

    for metric, value in test_metrics.items():
        print(
            f"{metric}: {value:.2f}"
        )

    feature_names = (
        preprocessor
        .get_feature_names_out()
    )

    aggregated_importance = (
        aggregate_feature_importance(
            feature_names,
            model.feature_importances_,
        )
    )

    print(
        "\nAggregated feature importance:"
    )

    print(
        aggregated_importance
        .to_string()
    )


if __name__ == "__main__":
    main()
    