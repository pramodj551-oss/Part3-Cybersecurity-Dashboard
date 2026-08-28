"""Prediction utilities for the cybersecurity dashboard."""

from typing import Union

import pandas as pd

from src.model_loader import ModelArtifactError, load_trained_model


class PredictionEngine:
    def __init__(self):
        self.model = load_trained_model()

    @staticmethod
    def validate_input(data):
        if data is None:
            raise ValueError("Input data cannot be None.")
        if isinstance(data, pd.Series):
            data = data.to_frame().T
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        if data.empty:
            raise ValueError("Input DataFrame is empty.")
        return data

    def _align_features(self, data: pd.DataFrame) -> pd.DataFrame:
        expected = getattr(self.model, "feature_names_in_", None)
        if expected is None:
            return data

        expected = list(expected)
        missing = [column for column in expected if column not in data.columns]
        extra = [column for column in data.columns if column not in expected]
        if missing:
            raise ValueError(
                "Input is missing model feature(s): " + ", ".join(map(str, missing))
            )
        return data[expected].copy()

    def predict(self, data: pd.DataFrame):
        data = self._align_features(self.validate_input(data))
        return self.model.predict(data)

    def predict_probability(self, data: pd.DataFrame):
        data = self._align_features(self.validate_input(data))
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(data)
        return None

    def predict_with_summary(self, data: pd.DataFrame) -> pd.DataFrame:
        data = self.validate_input(data)
        prediction = self.predict(data)
        result = data.copy()
        result["Predicted_Severity"] = prediction
        probability = self.predict_probability(data)
        if probability is not None:
            result["Confidence"] = probability.max(axis=1).round(4)
        return result


def predict_incident(input_data: Union[pd.DataFrame, pd.Series]):
    return PredictionEngine().predict_with_summary(input_data)
