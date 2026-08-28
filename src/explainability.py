"""Deterministic model explainability helpers for the dashboard.

The helper prefers model-native feature importance when available and falls back
 to absolute linear coefficients for supported estimators. Outputs are normalized
 to a stable feature/importance contract for dashboard consumption.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class ExplainabilityError(ValueError):
    """Raised when a model cannot provide supported feature importance."""


def _as_feature_names(feature_names) -> list[str]:
    names = [str(name) for name in feature_names]
    if not names:
        raise ExplainabilityError("At least one feature name is required.")
    if len(set(names)) != len(names):
        raise ExplainabilityError("Feature names must be unique.")
    return names


def extract_feature_importance(model, feature_names) -> pd.DataFrame:
    """Return deterministic feature/importance rows for a fitted estimator.

    Preferred source: ``feature_importances_`` (tree-based estimators).
    Fallback: absolute ``coef_`` (linear estimators, including multiclass models).
    """
    names = _as_feature_names(feature_names)

    if hasattr(model, "feature_importances_"):
        raw = model.feature_importances_
    elif hasattr(model, "coef_"):
        raw = abs(model.coef_)
        if getattr(raw, "ndim", 1) > 1:
            raw = raw.mean(axis=0)
    else:
        raise ExplainabilityError(
            "Model does not expose supported feature importance or coefficients."
        )

    values = [float(value) for value in raw]
    if len(values) != len(names):
        raise ExplainabilityError(
            f"Feature count ({len(names)}) does not match importance count ({len(values)})."
        )
    if any(value < 0 for value in values):
        raise ExplainabilityError("Feature importance values must be non-negative.")

    result = pd.DataFrame({"feature": names, "importance": values})
    return result.sort_values(
        ["importance", "feature"], ascending=[False, True], kind="mergesort"
    ).reset_index(drop=True)


def save_feature_importance(model, feature_names, output_path) -> pd.DataFrame:
    """Extract and persist the dashboard feature-importance contract."""
    result = extract_feature_importance(model, feature_names)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(path, index=False)
    return result
