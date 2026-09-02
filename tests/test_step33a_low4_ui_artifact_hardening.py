"""Regression tests for STEP 33-A LOW #4 UI artifact hardening."""

import json

import numpy as np
import pandas as pd
import pytest

from pages.Feature_Importance import _load_importance
from pages.Model_Performance import _normalize


def test_feature_importance_rejects_non_finite_values(tmp_path):
    artifact = tmp_path / "feature_importance.csv"
    pd.DataFrame(
        {"feature": ["safe_feature", "bad_feature"], "importance": [0.5, np.inf]}
    ).to_csv(artifact, index=False)

    with pytest.raises(ValueError, match="non-finite"):
        _load_importance(artifact)


def test_feature_importance_accepts_finite_values(tmp_path):
    artifact = tmp_path / "feature_importance.csv"
    pd.DataFrame(
        {"feature": ["a", "b"], "importance": [0.5, -0.25]}
    ).to_csv(artifact, index=False)

    result = _load_importance(artifact)
    assert result["Importance"].tolist() == [0.5, -0.25]


def test_model_performance_normalize_rejects_non_finite_values():
    metrics = {"MAE": np.nan, "RMSE": np.inf, "R2": -np.inf}
    assert _normalize(metrics) == {}


def test_model_performance_normalize_keeps_finite_values():
    metrics = {"MAE": 1.25, "RMSE": "2.5", "R2": 0.75}
    assert _normalize(metrics) == {"MAE": 1.25, "RMSE": 2.5, "R²": 0.75}


def test_model_performance_loader_does_not_expose_artifact_details(tmp_path):
    from pages import Model_Performance

    missing = tmp_path / "missing.json"
    original_report = Model_Performance.EVALUATION_REPORT
    original_metrics = Model_Performance.METRICS_OUTPUT
    Model_Performance.EVALUATION_REPORT = missing
    Model_Performance.METRICS_OUTPUT = missing
    try:
        with pytest.raises(FileNotFoundError, match="No usable regression metrics") as exc_info:
            Model_Performance._load_metrics()
        assert str(missing) not in str(exc_info.value)
    finally:
        Model_Performance.EVALUATION_REPORT = original_report
        Model_Performance.METRICS_OUTPUT = original_metrics
