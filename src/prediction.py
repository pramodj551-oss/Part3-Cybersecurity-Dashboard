"""
==========================================================
AI-Powered Cybersecurity Dashboard
Prediction Module
Version: 3.0
==========================================================
"""

from typing import Union

import pandas as pd

from src.model_loader import load_trained_model


class PredictionEngine:
    """
    Prediction engine for cybersecurity incident severity.
    """

    def __init__(self):

        self.model = load_trained_model()

    # ------------------------------------------------------
    # Validate Input
    # ------------------------------------------------------

    @staticmethod
    def validate_input(data):

        if data is None:
            raise ValueError("Input data cannot be None.")

        if isinstance(data, pd.Series):
            data = data.to_frame().T

        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Input must be a pandas DataFrame."
            )

        if data.empty:
            raise ValueError(
                "Input DataFrame is empty."
            )

        return data

    # ------------------------------------------------------
    # Predict Class
    # ------------------------------------------------------

    def predict(
        self,
        data: pd.DataFrame
    ):

        data = self.validate_input(data)

        predictions = self.model.predict(data)

        return predictions

    # ------------------------------------------------------
    # Predict Probability
    # ------------------------------------------------------

    def predict_probability(
        self,
        data: pd.DataFrame
    ):

        data = self.validate_input(data)

        if hasattr(self.model, "predict_proba"):

            return self.model.predict_proba(data)

        return None

    # ------------------------------------------------------
    # Human Readable Results
    # ------------------------------------------------------

    def predict_with_summary(
        self,
        data: pd.DataFrame
    ) -> pd.DataFrame:

        data = self.validate_input(data)

        prediction = self.predict(data)

        result = data.copy()

        result["Predicted_Severity"] = prediction

        probability = self.predict_probability(data)

        if probability is not None:

            result["Confidence"] = (
                probability.max(axis=1).round(4)
            )

        return result


# ----------------------------------------------------------
# Convenience Function
# ----------------------------------------------------------

def predict_incident(
    input_data: Union[pd.DataFrame, pd.Series]
):

    engine = PredictionEngine()

    return engine.predict_with_summary(input_data)


# ----------------------------------------------------------
# Standalone Testing
# ----------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("Prediction Module Loaded Successfully")
    print("=" * 60)

    print(
        "Use predict_incident() from the dashboard."
      )
