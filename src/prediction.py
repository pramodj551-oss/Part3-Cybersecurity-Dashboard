"""Part 2-compatible cybersecurity regression prediction engine."""

from typing import Union

import numpy as np
import pandas as pd

from config.config import (
    EXCLUDED_POST_INCIDENT_FEATURES,
    PREDICTION_FEATURES,
    PREDICTION_NUMERIC_LIMITS,
)
from src.model_loader import load_runtime_artifacts
from src.observability import elapsed_ms, emit_event, start_timer


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

        validated = data.copy()
        for column, (minimum, maximum) in PREDICTION_NUMERIC_LIMITS.items():
            try:
                values = pd.to_numeric(validated[column], errors="raise")
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Prediction feature '{column}' must contain numeric values."
                ) from error
            values = values.to_numpy(dtype=float, na_value=np.nan)
            if not np.isfinite(values).all():
                raise ValueError(
                    f"Prediction feature '{column}' contains NaN or infinite values."
                )
            if (values < minimum).any() or (values > maximum).any():
                raise ValueError(
                    f"Prediction feature '{column}' is outside the allowed range "
                    f"[{minimum:g}, {maximum:g}]."
                )
            validated[column] = values

        return validated

    def transform(self, data: pd.DataFrame):
        raw = self.validate_input(data)
        inference_input = raw.drop(
            columns=EXCLUDED_POST_INCIDENT_FEATURES + ["severity_score"],
            errors="ignore",
        )
        transformed = self.preprocessor.transform(inference_input)

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
        # Part 2's LinearRegression artifact was fitted without pandas feature
        # names. Pass the deterministically aligned matrix as a NumPy array to
        # keep inference representation consistent with training and suppress
        # the sklearn feature-name warning without changing feature order.
        aligned = self.transform(data)
        return self.model.predict(aligned.to_numpy())

    def predict_with_summary(self, data: pd.DataFrame) -> pd.DataFrame:
        raw = self.validate_input(data)
        result = raw.copy()
        result["Predicted_Severity_Score"] = self.predict(raw)
        return result


def predict_incident(input_data: Union[pd.DataFrame, pd.Series]):
    """Run prediction while emitting safe structured success/failure events."""
    started = start_timer()
    rows = len(input_data) if hasattr(input_data, "__len__") else 0
    columns = len(input_data.columns) if isinstance(input_data, pd.DataFrame) else 0
    emit_event("prediction_started", "started", rows=rows, columns=columns)
    try:
        result = PredictionEngine().predict_with_summary(input_data)
    except ValueError:
        emit_event(
            "prediction_validation_failure",
            "failure",
            error_category="validation",
            duration_ms=elapsed_ms(started),
            rows=rows,
            columns=columns,
        )
        raise
    except FileNotFoundError:
        emit_event(
            "prediction_runtime_failure",
            "failure",
            error_category="artifact_unavailable",
            duration_ms=elapsed_ms(started),
            rows=rows,
            columns=columns,
        )
        raise
    except RuntimeError:
        emit_event(
            "prediction_runtime_failure",
            "failure",
            error_category="runtime_validation",
            duration_ms=elapsed_ms(started),
            rows=rows,
            columns=columns,
        )
        raise
    except Exception:
        emit_event(
            "prediction_runtime_failure",
            "failure",
            error_category="unexpected",
            duration_ms=elapsed_ms(started),
            rows=rows,
            columns=columns,
        )
        raise

    emit_event(
        "prediction_success",
        "success",
        duration_ms=elapsed_ms(started),
        rows=rows,
        columns=columns,
        prediction_count=len(result),
    )
    return result
