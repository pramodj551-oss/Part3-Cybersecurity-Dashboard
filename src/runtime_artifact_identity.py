"""Verify runtime artifact byte identity against the committed manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from config.config import BASE_DIR

EXPECTED_ARTIFACTS = (
    "models/best_model.pkl",
    "models/preprocessor.pkl",
    "models/feature_columns.pkl",
    "outputs/evaluation_report.json",
    "outputs/metrics.json",
    "outputs/feature_importance.csv",
)
MANIFEST_PATH = BASE_DIR / "models" / "artifact_manifest.json"


def verify_runtime_artifact_identity() -> tuple[bool, dict[str, str], str]:
    """Hash deployed runtime files and compare them with artifact_manifest.json."""
    if not MANIFEST_PATH.is_file():
        return False, {}, f"Missing runtime manifest: {MANIFEST_PATH}"

    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, {}, f"Invalid runtime manifest: {exc}"

    expected = manifest.get("files")
    if not isinstance(expected, dict) or set(expected) != set(EXPECTED_ARTIFACTS):
        return False, {}, "Runtime manifest must contain exactly the six expected artifacts"

    actual_hashes: dict[str, str] = {}
    mismatches: list[str] = []
    for relative in EXPECTED_ARTIFACTS:
        path = BASE_DIR / relative
        if not path.is_file() or path.stat().st_size == 0:
            mismatches.append(f"missing/empty: {relative}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        actual_hashes[relative] = actual
        if actual != expected[relative]:
            mismatches.append(
                f"hash mismatch: {relative} ({actual} != {expected[relative]})"
            )

    if mismatches:
        return False, actual_hashes, "; ".join(mismatches)

    return True, actual_hashes, "6/6 runtime artifacts exactly match artifact_manifest.json"
