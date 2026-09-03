"""Adversarial tests for the hard model-inference execution boundary."""

import time
from pathlib import Path

import numpy as np
import pytest

from src.prediction import _isolated_model_predict


class FastTestModel:
    """Pickle-safe test model used to prove normal isolated inference."""

    def predict(self, values):
        return np.full(len(values), 42.0)


class HangingTestModel:
    """Test model that must be terminated before its side effect occurs."""

    def __init__(self, marker: str):
        self.marker = marker

    def predict(self, values):
        time.sleep(30)
        Path(self.marker).write_text("completed", encoding="utf-8")
        return np.zeros(len(values))


def test_isolated_prediction_returns_normal_result():
    result = _isolated_model_predict(
        FastTestModel(),
        np.zeros((2, 3)),
        timeout_seconds=2.0,
    )
    assert result.tolist() == [42.0, 42.0]


def test_isolated_prediction_hard_timeout_terminates_worker(tmp_path):
    marker = tmp_path / "should-not-be-created.txt"
    started = time.monotonic()

    with pytest.raises(TimeoutError, match="execution deadline"):
        _isolated_model_predict(
            HangingTestModel(str(marker)),
            np.zeros((1, 3)),
            timeout_seconds=0.25,
        )

    elapsed = time.monotonic() - started
    assert elapsed < 5.0
    assert not marker.exists()


def test_isolated_prediction_rejects_non_positive_timeout():
    with pytest.raises(ValueError, match="greater than zero"):
        _isolated_model_predict(FastTestModel(), np.zeros((1, 1)), 0.0)
