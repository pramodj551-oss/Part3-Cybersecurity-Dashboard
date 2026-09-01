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
        inference_input = raw.drop(
            columns=EXCLUDED_POST_INCIDENT_FEATURES + ["severity_score"],
            errors="ignore",
        )
        transformed = self.preprocessor.transform(inference_input)

        # The fitted preprocessor owns the authoritative transformed schema.
        # The model is trained on the selected subset persisted in
        # feature_columns.pkl, so first name the full transformed matrix from
        # the preprocessor and only then select/reorder the model contract.
        try:
            transformed_names = list(self.preprocessor.get_feature_names_out())
        except AttributeError as error:
            raise RuntimeError(
                "Part 2 preprocessor does not expose get_feature_names_out(); "
                "cannot deterministically align transformed features."
            ) from error

        if len(transformed_names) != transformed.shape[1]:
            raise RuntimeError(
                "Preprocessor feature-name count does not match transformed "
                f"matrix width: names={len(transformed_names)}, "
                f"columns={transformed.shape[1]}."
            )
        if len(set(transformed_names)) != len(transformed_names):
            raise RuntimeError("Preprocessor returned duplicate transformed feature names.")

        if hasattr(transformed, "toarray"):
            transformed = transformed.toarray()
        aligned = pd.DataFrame(transformed, columns=transformed_names, index=raw.index)

        missing = [c for c in self.feature_columns if c not in aligned.columns]
        if missing:
            raise ValueError(
                "Transformed data is missing required features: "
                + ", ".join(map(str, missing))
            )
        return aligned.loc[:, self.feature_columns]

    def predict(self, data: pd.DataFrame):
        return self.model.predict(self.transform(data))

    def predict_with_summary(self, data: pd.DataFrame) -> pd.DataFrame:
        raw = self.validate_input(data)
        result = raw.copy()
        result["Predicted_Severity_Score"] = self.predict(raw)
        return result


def predict_incident(input_data: Union[pd.DataFrame, pd.Series]):
    return PredictionEngine().predict_with_summary(input_data)
