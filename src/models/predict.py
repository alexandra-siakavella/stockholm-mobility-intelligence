"""
Generate delay predictions using the trained XGBoost model.
"""

from pathlib import Path

import joblib
import pandas as pd


MODEL_DIR = Path("data/models")

MODEL_PATH = MODEL_DIR / "delay_xgboost.joblib"
PREPROCESSOR_PATH = MODEL_DIR / "delay_preprocessor.joblib"


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


def load_model():
    """Load the trained model and preprocessor."""

    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(
        PREPROCESSOR_PATH
    )

    return model, preprocessor


def predict_delay(
    data: pd.DataFrame,
) -> pd.Series:
    """Predict departure delay in seconds."""

    model, preprocessor = load_model()

    features = data[FEATURES]

    encoded_features = preprocessor.transform(
        features
    )

    predictions = model.predict(
        encoded_features
    )

    return pd.Series(
        predictions,
        index=data.index,
        name="predicted_delay_seconds",
    )


def main() -> None:
    """Run an example prediction."""

    example = pd.DataFrame(
        [
            {
                "site_id": 9001,
                "line_designation": "14",
                "transport_mode": "METRO",
                "destination": "T-Centralen",
                "direction": "North",
                "minutes_until_departure": 5.0,
                "observation_hour": 8,
                "observation_day_of_week": 1,
                "is_peak_hour": True,
            }
        ]
    )

    predictions = predict_delay(
        example
    )

    print(
        "Predicted delay:"
    )

    print(
        f"{predictions.iloc[0]:.2f} seconds"
    )


if __name__ == "__main__":
    main()
    