"""Prediction-input validation for the Part 3 dashboard.

The fitted preprocessing object from Part 2 is authoritative at inference time.
This module deliberately does not fit LabelEncoder/Scaler objects on dashboard
inputs, because doing so would create an inference-time training path and can
produce category/feature mappings that differ from the trained model.
"""

import pandas as pd


class DashboardPreprocessor:
    """Validate raw dashboard input without fitting a new preprocessing model."""

    @staticmethod
    def validate(data: pd.DataFrame) -> pd.DataFrame:
        if data is None:
            raise ValueError("Input data cannot be None.")
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        if data.empty:
            raise ValueError("Input DataFrame is empty.")
        return data.copy()

    @staticmethod
    def handle_missing_values(data: pd.DataFrame) -> pd.DataFrame:
        """Return validated input unchanged; Part 2 owns missing-value fitting."""
        return DashboardPreprocessor.validate(data)

    def encode_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prevent unsafe inference-time category fitting."""
        raise RuntimeError(
            "DashboardPreprocessor does not fit encoders at inference time. "
            "Use the fitted Part 2 preprocessor through src.prediction."
        )

    def preprocess(self, data: pd.DataFrame) -> pd.DataFrame:
        """Validate raw input; transformation must be performed by Part 2."""
        return self.validate(data)


def prepare_input(data: pd.DataFrame) -> pd.DataFrame:
    """Backward-compatible validation helper; no inference-time fitting occurs."""
    return DashboardPreprocessor().preprocess(data)


if __name__ == "__main__":
    sample = pd.DataFrame({
        "sector": ["Energy"],
        "region": ["Asia Pacific"],
        "attack_type": ["Phishing"],
        "threat_actor": ["State-Sponsored"],
        "records_affected": [100991],
        "detection_time_hours": [26.48],
        "ransom_demand_usd": [1393],
        "data_exfiltration": [0],
        "zero_day_used": [0],
    })
    print(DashboardPreprocessor().preprocess(sample))
