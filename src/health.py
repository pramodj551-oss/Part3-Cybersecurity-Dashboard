"""Production liveness/readiness checks for the Streamlit dashboard."""

from __future__ import annotations

import json
import time
from typing import Any

from src.deployment_fingerprint import get_runtime_commit
from src.model_loader import load_runtime_artifacts
from src.runtime_artifact_identity import verify_runtime_artifact_identity

HEALTH_CONTRACT_VERSION = "1"


def liveness() -> dict[str, Any]:
    """Return a process-level liveness response without loading artifacts."""
    return {"status": "ok", "check": "liveness", "contract_version": HEALTH_CONTRACT_VERSION}


def _artifact_readiness() -> dict[str, Any]:
    """Verify runtime artifact identity before deserialization."""
    try:
        verified, hashes, _message = verify_runtime_artifact_identity()
        return {
            "status": "ready" if verified else "not_ready",
            "identity_verified": bool(verified),
            "verified_files": len(hashes) if verified else 0,
        }
    except Exception:
        return {"status": "not_ready", "identity_verified": False, "verified_files": 0}


def _model_readiness() -> dict[str, Any]:
    """Load verified runtime artifacts and validate their callable interfaces."""
    try:
        model, preprocessor, feature_columns = load_runtime_artifacts()
        model_ok = callable(getattr(model, "predict", None))
        preprocessor_ok = callable(getattr(preprocessor, "transform", None))
        feature_count = len(feature_columns) if feature_columns else 0
        ready = model_ok and preprocessor_ok and feature_count > 0
        return {
            "status": "ready" if ready else "not_ready",
            "model_predict_callable": model_ok,
            "preprocessor_transform_callable": preprocessor_ok,
            "feature_columns": feature_count,
        }
    except Exception:
        return {
            "status": "not_ready",
            "model_predict_callable": False,
            "preprocessor_transform_callable": False,
            "feature_columns": 0,
        }


def readiness() -> dict[str, Any]:
    """Return a machine-readable readiness contract for production traffic."""
    artifact = _artifact_readiness()
    model = (
        _model_readiness()
        if artifact["status"] == "ready"
        else {
            "status": "not_ready",
            "model_predict_callable": False,
            "preprocessor_transform_callable": False,
            "feature_columns": 0,
        }
    )
    ready = artifact["status"] == "ready" and model["status"] == "ready"
    return {
        "status": "ready" if ready else "not_ready",
        "check": "readiness",
        "contract_version": HEALTH_CONTRACT_VERSION,
        "runtime_commit": get_runtime_commit(),
        "artifacts": artifact,
        "model": model,
    }


def health_snapshot() -> dict[str, Any]:
    """Return the complete machine-readable health snapshot."""
    started = time.monotonic()
    live = liveness()
    ready = readiness()
    return {
        "status": "ready" if ready["status"] == "ready" else "not_ready",
        "contract_version": HEALTH_CONTRACT_VERSION,
        "runtime_commit": ready["runtime_commit"],
        "liveness": live,
        "readiness": ready,
        "duration_ms": round((time.monotonic() - started) * 1000, 3),
    }


def health_json() -> str:
    """Serialize the health snapshot deterministically for machine consumption."""
    return json.dumps(health_snapshot(), sort_keys=True, separators=(",", ":"))
