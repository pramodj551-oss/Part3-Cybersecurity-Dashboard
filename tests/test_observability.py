"""Dedicated tests for structured runtime prediction observability."""

import json
import logging

import pandas as pd
import pytest

import src.prediction as prediction
from src.observability import emit_event


def _valid_input():
    return pd.DataFrame({"required": [1]})


def test_emit_event_is_valid_json_and_excludes_unapproved_fields(caplog):
    with caplog.at_level(logging.INFO, logger="part3.runtime"):
        payload = emit_event(
            "test_event",
            "success",
            rows=2,
            secret="must-not-appear",
        )

    assert payload["event"] == "test_event"
    assert payload["status"] == "success"
    assert payload["rows"] == 2
    assert "secret" not in payload
    parsed = json.loads(caplog.records[-1].message)
    assert parsed == payload
    assert "must-not-appear" not in caplog.text


def test_prediction_success_emits_structured_event(monkeypatch, caplog):
    class FakeEngine:
        def predict_with_summary(self, data):
            return pd.DataFrame({"Predicted_Severity_Score": [4.5]})

    monkeypatch.setattr(prediction, "PredictionEngine", FakeEngine)
    with caplog.at_level(logging.INFO, logger="part3.runtime"):
        result = prediction.predict_incident(_valid_input())

    assert len(result) == 1
    events = [json.loads(record.message) for record in caplog.records]
    assert [event["event"] for event in events] == [
        "prediction_started",
        "prediction_success",
    ]
    assert events[-1]["status"] == "success"
    assert events[-1]["prediction_count"] == 1
    assert events[-1]["duration_ms"] >= 0


def test_prediction_validation_failure_emits_safe_event(monkeypatch, caplog):
    class FakeEngine:
        def predict_with_summary(self, data):
            raise ValueError("SECRET_INTERNAL_VALIDATION_DETAIL")

    monkeypatch.setattr(prediction, "PredictionEngine", FakeEngine)
    with caplog.at_level(logging.INFO, logger="part3.runtime"):
        with pytest.raises(ValueError):
            prediction.predict_incident(_valid_input())

    events = [json.loads(record.message) for record in caplog.records]
    assert events[-1]["event"] == "prediction_validation_failure"
    assert events[-1]["error_category"] == "validation"
    assert events[-1]["duration_ms"] >= 0
    assert "SECRET_INTERNAL_VALIDATION_DETAIL" not in caplog.text


def test_prediction_runtime_failure_emits_category_without_exception_details(
    monkeypatch, caplog
):
    class FakeEngine:
        def predict_with_summary(self, data):
            raise RuntimeError("SECRET_RUNTIME_DETAIL")

    monkeypatch.setattr(prediction, "PredictionEngine", FakeEngine)
    with caplog.at_level(logging.INFO, logger="part3.runtime"):
        with pytest.raises(RuntimeError):
            prediction.predict_incident(_valid_input())

    events = [json.loads(record.message) for record in caplog.records]
    assert events[-1]["event"] == "prediction_runtime_failure"
    assert events[-1]["error_category"] == "runtime_validation"
    assert "SECRET_RUNTIME_DETAIL" not in caplog.text
