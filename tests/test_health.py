"""Tests for the production health/readiness contract."""

import json

import pytest

import src.health as health


def test_liveness_is_process_safe_and_machine_readable():
    result = health.liveness()
    assert result == {
        "status": "ok",
        "check": "liveness",
        "contract_version": "1",
    }


def test_readiness_reports_current_runtime_commit(monkeypatch):
    monkeypatch.setattr(health, "get_runtime_commit", lambda: "test-commit")
    monkeypatch.setattr(
        health,
        "verify_runtime_artifact_identity",
        lambda: {"models/best_model.pkl": "ok"},
    )
    result = health.readiness()
    assert result["status"] == "ready"
    assert result["runtime_commit"] == "test-commit"
    assert result["artifacts"]["status"] == "ready"
    assert result["model"]["status"] == "ready"


def test_readiness_fails_closed_on_artifact_verification_error(monkeypatch):
    def fail_verification():
        raise RuntimeError("artifact failure")

    monkeypatch.setattr(health, "verify_runtime_artifact_identity", fail_verification)
    result = health.readiness()
    assert result["status"] == "not_ready"
    assert result["artifacts"]["identity_verified"] is False


def test_readiness_fails_when_model_file_is_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(health, "verify_runtime_artifact_identity", lambda: True)
    monkeypatch.setattr(health, "MODEL_PATH", tmp_path / "missing-model.pkl")
    monkeypatch.setattr(health, "PREPROCESSOR_PATH", tmp_path / "preprocessor.pkl")
    monkeypatch.setattr(health, "FEATURE_COLUMNS_PATH", tmp_path / "feature_columns.pkl")
    health.PREPROCESSOR_PATH.write_bytes(b"x")
    health.FEATURE_COLUMNS_PATH.write_bytes(b"x")

    result = health.readiness()
    assert result["status"] == "not_ready"
    assert "model" in result["model"]["missing_or_empty"]


def test_health_snapshot_contains_liveness_and_readiness(monkeypatch):
    monkeypatch.setattr(health, "get_runtime_commit", lambda: "test-commit")
    snapshot = health.health_snapshot()
    assert snapshot["runtime_commit"] == "test-commit"
    assert snapshot["liveness"]["status"] == "ok"
    assert snapshot["readiness"]["status"] in {"ready", "not_ready"}
    assert snapshot["duration_ms"] >= 0


def test_health_json_is_valid_json_and_has_stable_machine_contract():
    payload = health.health_json()
    parsed = json.loads(payload)
    assert parsed["contract_version"] == "1"
    assert set(parsed) == {
        "status",
        "contract_version",
        "runtime_commit",
        "liveness",
        "readiness",
        "duration_ms",
    }


def test_health_snapshot_does_not_expose_exception_details(monkeypatch):
    def fail_verification():
        raise RuntimeError("SECRET_INTERNAL_EXCEPTION")

    monkeypatch.setattr(health, "verify_runtime_artifact_identity", fail_verification)
    payload = health.health_json()
    assert "SECRET_INTERNAL_EXCEPTION" not in payload
