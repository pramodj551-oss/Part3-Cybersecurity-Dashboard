"""
==========================================================
AI-Powered Cybersecurity Dashboard
Preprocessing Module
Version: 3.0
==========================================================
"""

from typing import Optional

import pandas as pd
from sklearn.preprocessing import LabelEncoder


class DashboardPreprocessor:
    """
    Preprocess user input before prediction.
    """

    def __init__(self):

        self.encoders = {}

    # ------------------------------------------------------
    # Validate Input
    # ------------------------------------------------------

    @staticmethod
    def validate(data: pd.DataFrame) -> pd.DataFrame:

        if data is None:
            raise ValueError("Input data cannot be None.")

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
    # Missing Values
    # ------------------------------------------------------

    @staticmethod
    def handle_missing_values(
        data: pd.DataFrame
    ) -> pd.DataFrame:

        processed = data.copy()

        numeric_columns = processed.select_dtypes(
            include=["number"]
        ).columns

        categorical_columns = processed.select_dtypes(
            include=["object", "category"]
        ).columns

        for column in numeric_columns:

            processed[column] = processed[column].fillna(
                processed[column].median()
            )

        for column in categorical_columns:

            processed[column] = processed[column].fillna(
                "Unknown"
            )

        return processed

    # ------------------------------------------------------
    # Encode Categories
    # ------------------------------------------------------

    def encode_features(
        self,
        data: pd.DataFrame
    ) -> pd.DataFrame:

        processed = data.copy()

        categorical_columns = processed.select_dtypes(
            include=["object", "category"]
        ).columns

        for column in categorical_columns:

            encoder = LabelEncoder()

            processed[column] = encoder.fit_transform(
                processed[column].astype(str)
            )

            self.encoders[column] = encoder

        return processed

    # ------------------------------------------------------
    # Final Preparation
    # ------------------------------------------------------

    def preprocess(
        self,
        data: pd.DataFrame
    ) -> pd.DataFrame:

        data = self.validate(data)

        data = self.handle_missing_values(data)

        data = self.encode_features(data)

        return data


# ----------------------------------------------------------
# Convenience Function
# ----------------------------------------------------------

def prepare_input(
    data: pd.DataFrame
) -> pd.DataFrame:

    processor = DashboardPreprocessor()

    return processor.preprocess(data)


# ----------------------------------------------------------
# Standalone Test
# ----------------------------------------------------------

if __name__ == "__main__":

    sample = pd.DataFrame({
        "Protocol": ["TCP"],
        "Country": ["India"],
        "Packets": [250]
    })

    processed = prepare_input(sample)

    print("=" * 60)
    print("PREPROCESSING COMPLETED")
    print("=" * 60)

    print(processed)
