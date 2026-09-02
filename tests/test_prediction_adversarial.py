"""Adversarial production-boundary tests for prediction and artifact loading.

These tests intentionally use the real PredictionEngine/runtime artifacts when
available in CI. They do not introduce executable pickle payloads.
"""

from pathlib import Path
import io
import pickle

import pandas as pd
import pytest

from config.config import DATASET_PATH, PREDICTION_FEATURES
from src.model_loader import ModelLoader
from src.prediction import PredictionEngine
from src.upload_validation import validate_upload_size


ROOT = Path(__file__).resolve().parents[1]


def _valid_prediction_frame() -> pd.DataFrame:
    source = pd.read_csv(DATASET_PATH, nrows=1)
    missing = [c for c in PREDICTION_FEATURES if c not in source.columns]
    if missing:
        pytest.fail(f"Production dataset is missing prediction features: {missing}")
    return source.loc[:, PREDICTION_FEATURES].copy()


def test_extra_columns_do_not_change_prediction_contract():
    """Unexpected columns must not alter the trained feature alignment."""
    base = _valid_prediction_frame()
    extra = base.copy()
    extra["unexpected_column"] = "attacker-controlled-value"

    engine = PredictionEngine()
    base_prediction = engine.predict(base)
    extra_prediction = engine.predict(extra)

    assert len(base_prediction) == len(extra_prediction) == 1
    assert float(base_prediction[0]) == pytest.approx(float(extra_prediction[0]))


def test_non_numeric_required_feature_fails_closed():
    """A numeric production feature must not silently become a prediction."""
    data = _valid_prediction_frame()
    data.loc[0, "records_affected"] = "definitely-not-a-number"

    with pytest.raises((ValueError, TypeError, RuntimeError)):
        PredictionEngine().predict(data)


def test_malformed_numeric_values_fail_closed():
    """NaN/inf numeric inputs must not yield a normal prediction."""
    for value in [float("nan"), float("inf"), float("-inf")]:
        data = _valid_prediction_frame()
        data.loc[0, "records_affected"] = value
        with pytest.raises((ValueError, TypeError, RuntimeError)):
            PredictionEngine().predict(data)


def test_empty_prediction_frame_is_rejected():
    with pytest.raises(ValueError, match="empty"):
        PredictionEngine.validate_input(pd.DataFrame(columns=PREDICTION_FEATURES))


def test_missing_required_prediction_feature_is_rejected():
    data = _valid_prediction_frame().drop(columns=[PREDICTION_FEATURES[0]])
    with pytest.raises(ValueError, match="missing required prediction features"):
        PredictionEngine.validate_input(data)


def test_malformed_csv_is_rejected_at_parse_boundary():
    """CSV parsing must fail or produce a frame that the prediction boundary rejects."""
    malformed = io.BytesIO(b"a,b\n1,\"unterminated\n")
    try:
        parsed = pd.read_csv(malformed)
    except Exception:
        return
    with pytest.raises((ValueError, TypeError, RuntimeError)):
        PredictionEngine.validate_input(parsed)


def test_empty_csv_is_rejected_at_prediction_boundary():
    empty_csv = io.StringIO(",".join(PREDICTION_FEATURES) + "\n")
    parsed = pd.read_csv(empty_csv)
    with pytest.raises(ValueError, match="empty"):
        PredictionEngine.validate_input(parsed)


def test_malformed_date_is_not_treated_as_a_prediction_feature():
    """The prediction contract is intentionally limited to PREDICTION_FEATURES.

    This test documents that incident_date is outside the prediction contract;
    malformed metadata must therefore not become an alternate inference path.
    """
    data = _valid_prediction_frame()
    data["incident_date"] = "not-a-date"
    result = PredictionEngine().predict(data)
    assert len(result) == 1
    assert pd.notna(result[0])


def test_model_loader_rejects_non_pickle_model_without_execution():
    """Invalid artifact bytes must fail closed without an executable payload."""
    tmp = ROOT / ".pytest_adversarial_tmp"
    tmp.mkdir(exist_ok=True)
    try:
        model_path = tmp / "best_model.pkl"
        preprocessor_path = tmp / "preprocessor.pkl"
        feature_columns_path = tmp / "feature_columns.pkl"

        model_path.write_bytes(b"this-is-not-a-valid-pickle")
        preprocessor_path.write_bytes(pickle.dumps({"safe": True}))
        feature_columns_path.write_bytes(pickle.dumps(["records_affected"]))

        loader = ModelLoader(
            model_path=model_path,
            preprocessor_path=preprocessor_path,
            feature_columns_path=feature_columns_path,
        )
        with pytest.raises(RuntimeError, match="Unable to load Part 2 artifacts"):
            loader.load()
    finally:
        for path in tmp.glob("*"):
            path.unlink()
        tmp.rmdir()


def test_upload_size_boundary_remains_enforced():
    class Upload:
        size = 100 * 1024 * 1024 + 1

    with pytest.raises(ValueError, match="100 MB limit"):
        validate_upload_size(Upload(), 100)
