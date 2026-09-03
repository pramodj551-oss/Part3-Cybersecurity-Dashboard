"""Production liveness/readiness checks for the Streamlit dashboard.

The health contract is deliberately side-effect free and returns JSON-safe
Python primitives so it can be rendered by Streamlit or consumed by a future
HTTP health adapter without changing prediction behavior.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from config.config import (
    FEATURE_COLUMNS_PATH,
    MODEL_PATH,
    PREPROCESSOR_PATH,
)
from src.deployment_fingerprint import get_runtime_commit
from src.runtime_artifact_identity import verify_runtime_artifact_identity


HEALTH_CONTRACT_VERSION = "1"


def liveness() -> dict[str, Any]:
    """Return a process-level liveness response without loading model artifacts."""
    return {
        "status": "ok",
        "check": "liveness",
        "contract_version": HEALTH_CONTRACT_VERSION,
    }


def _artifact_readiness() -> dict[str, Any]:
    """Verify the immutable production artifact contract without deserializing it."""
    try:
        verification = verify_runtime_artifact_identity()
        return {
            "status": "ready" if verification else "not_ready",
            "identity_verified": bool(verification),
        }
    except Exception:
        return {
            "status": "not_ready",
            "identity_verified": False,
        }


def _model_readiness() -> dict[str, Any]:
    """Check required model files exist and are non-empty, without loading pickle."""
    paths = {
        "model": MODEL_PATH,
        "preprocessor": PREPROCESSOR_PATH,
        "feature_columns": FEATURE_COLUMNS_PATH,
    }
    missing_or_empty = [
        name for name, path in paths.items()
        if not path.is_file() or path.stat().st_size <= 0
    ]
    return {
        "status": "ready" if not missing_or_empty else "not_ready",
        "missing_or_empty": missing_or_empty,
    }


def readiness() -> dict[str, Any]:
    """Return a machine-readable readiness contract for production traffic."""
    artifact = _artifact_readiness()
    model = _model_readiness()
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
