"""Part 2-compatible cybersecurity regression prediction engine."""

from typing import Union

import pandas as pd

from config.config import EXCLUDED_POST_INCIDENT_FEATURES, PREDICTION_FEATURES
from src.model_loader import load_runtime_artifacts


class PredictionEngine:
    """Run inference using only the fitted Part 2 runtime artifacts."""

    def __init__(self):
        self.model, self.preprocessor, self.feature_columns = load_runtime_artifacts()

    @staticmethod
    def validate_input(data):
        if isinstance(data, pd.Series):
            data = data.to_frame().T
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        if data.empty:
            raise ValueError("Input DataFrame is empty.")
        missing = [column for column in PREDICTION_FEATURES if column not in data.columns]
        if missing:
            raise ValueError(
                "Input is missing required prediction features: "
                + ", ".join(missing)
            )
        return data.copy()

    def transform(self, data: pd.DataFrame):
        raw = self.validate_input(data)
        # These fields are allowed in an uploaded historical dataset but are
        # explicitly excluded from the prediction contract to prevent leakage.
        inference_input = raw.drop(
            columns=EXCLUDED_POST_INCIDENT_FEATURES + ["severity_score"],
            errors="ignore",
        )
        transformed = self.preprocessor.transform(inference_input)
        if not isinstance(transformed, pd.DataFrame):
            transformed = pd.DataFrame(transformed)
        if len(self.feature_columns) == transformed.shape[1]:
            transformed.columns = self.feature_columns
        missing = [c for c in self.feature_columns if c not in transformed.columns]
        if missing:
            raise ValueError(
                "Transformed data is missing required features: "
                + ", ".join(map(str, missing))
            )
        return transformed.loc[:, self.feature_columns]

    def predict(self, data: pd.DataFrame):
        return self.model.predict(self.transform(data))

    def predict_with_summary(self, data: pd.DataFrame) -> pd.DataFrame:
        raw = self.validate_input(data)
        result = raw.copy()
        result["Predicted_Severity_Score"] = self.predict(raw)
        return result


def predict_incident(input_data: Union[pd.DataFrame, pd.Series]):
    return PredictionEngine().predict_with_summary(input_data)
