"""Adversarial tests for the runtime artifact SHA-256 identity gate."""

import hashlib
import json
from pathlib import Path

import pytest

from src import model_loader
from src import runtime_artifact_identity as identity


ARTIFACTS = tuple(identity.EXPECTED_ARTIFACTS)


def _build_runtime(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    """Create a synthetic six-file runtime and a matching manifest."""
    hashes = {}
    for index, relative in enumerate(ARTIFACTS):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = f"trusted-artifact-{index}".encode()
        path.write_bytes(payload)
        hashes[relative] = hashlib.sha256(payload).hexdigest()

    manifest = {
        "source_release_tag": "test-release",
        "files": hashes,
    }
    manifest_path = tmp_path / "models" / "artifact_manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path, hashes


def _patch_runtime(monkeypatch, tmp_path: Path, manifest_path: Path) -> None:
    monkeypatch.setattr(identity, "BASE_DIR", tmp_path)
    monkeypatch.setattr(identity, "MANIFEST_PATH", manifest_path)


def test_valid_manifest_has_exact_six_of_six_matches(monkeypatch, tmp_path):
    manifest_path, _ = _build_runtime(tmp_path)
    _patch_runtime(monkeypatch, tmp_path, manifest_path)

    ok, hashes, message = identity.verify_runtime_artifact_identity()

    assert ok is True
    assert len(hashes) == 6
    assert message == "6/6 runtime artifacts exactly match artifact_manifest.json"


def test_one_artifact_byte_modification_fails_closed(monkeypatch, tmp_path):
    manifest_path, _ = _build_runtime(tmp_path)
    _patch_runtime(monkeypatch, tmp_path, manifest_path)
    target = tmp_path / "models/best_model.pkl"
    target.write_bytes(target.read_bytes() + b"-tampered")

    ok, hashes, message = identity.verify_runtime_artifact_identity()

    assert ok is False
    assert hashes["models/best_model.pkl"]
    assert "hash mismatch: models/best_model.pkl" in message


def test_manifest_hash_modification_fails_closed(monkeypatch, tmp_path):
    manifest_path, hashes = _build_runtime(tmp_path)
    hashes["models/best_model.pkl"] = "0" * 64
    manifest_path.write_text(
        json.dumps({"source_release_tag": "test-release", "files": hashes}),
        encoding="utf-8",
    )
    _patch_runtime(monkeypatch, tmp_path, manifest_path)

    ok, _, message = identity.verify_runtime_artifact_identity()

    assert ok is False
    assert "hash mismatch: models/best_model.pkl" in message


def test_missing_manifest_fails_closed(monkeypatch, tmp_path):
    manifest_path = tmp_path / "models" / "artifact_manifest.json"
    _patch_runtime(monkeypatch, tmp_path, manifest_path)

    ok, hashes, message = identity.verify_runtime_artifact_identity()

    assert ok is False
    assert hashes == {}
    assert "Missing runtime manifest" in message


def test_extra_manifest_artifact_fails_closed(monkeypatch, tmp_path):
    manifest_path, hashes = _build_runtime(tmp_path)
    hashes["models/attacker_added.pkl"] = "0" * 64
    manifest_path.write_text(
        json.dumps({"source_release_tag": "test-release", "files": hashes}),
        encoding="utf-8",
    )
    _patch_runtime(monkeypatch, tmp_path, manifest_path)

    ok, _, message = identity.verify_runtime_artifact_identity()

    assert ok is False
    assert "exactly the six expected artifacts" in message


@pytest.mark.parametrize("mode", ["missing", "empty"])
def test_missing_or_empty_artifact_fails_closed(monkeypatch, tmp_path, mode):
    manifest_path, _ = _build_runtime(tmp_path)
    _patch_runtime(monkeypatch, tmp_path, manifest_path)
    target = tmp_path / "models/preprocessor.pkl"
    if mode == "missing":
        target.unlink()
    else:
        target.write_bytes(b"")

    ok, _, message = identity.verify_runtime_artifact_identity()

    assert ok is False
    assert "missing/empty: models/preprocessor.pkl" in message


@pytest.mark.parametrize(
    "manifest_payload",
    [
        {"files": []},
        {"files": {"models/best_model.pkl": "bad"}},
        {"source_release_tag": "test-release"},
        {"files": None},
    ],
)
def test_wrong_manifest_structure_fails_closed(monkeypatch, tmp_path, manifest_payload):
    manifest_path, _ = _build_runtime(tmp_path)
    manifest_path.write_text(json.dumps(manifest_payload), encoding="utf-8")
    _patch_runtime(monkeypatch, tmp_path, manifest_path)

    ok, _, message = identity.verify_runtime_artifact_identity()

    assert ok is False
    assert "exactly the six expected artifacts" in message


def test_runtime_loader_refuses_to_deserialize_when_identity_fails(monkeypatch):
    monkeypatch.setattr(
        model_loader,
        "verify_runtime_artifact_identity",
        lambda: (False, {}, "hash mismatch: models/best_model.pkl"),
    )
    load_called = False

    def fail_if_called(self):
        nonlocal load_called
        load_called = True
        raise AssertionError("ModelLoader must not deserialize unverified artifacts")

    monkeypatch.setattr(model_loader.ModelLoader, "get_artifacts", fail_if_called)

    with pytest.raises(model_loader.ModelArtifactError, match="identity verification failed"):
        model_loader.load_runtime_artifacts()

    assert load_called is False


def test_direct_model_loader_refuses_to_deserialize_when_identity_fails(monkeypatch, tmp_path):
    """Direct ModelLoader.load() must enforce the identity gate before deserialization."""
    model_path = tmp_path / "best_model.pkl"
    preprocessor_path = tmp_path / "preprocessor.pkl"
    feature_columns_path = tmp_path / "feature_columns.pkl"
    for path in (model_path, preprocessor_path, feature_columns_path):
        path.write_bytes(b"untrusted-artifact")

    monkeypatch.setattr(
        model_loader,
        "verify_runtime_artifact_identity",
        lambda: (False, {}, "hash mismatch: models/best_model.pkl"),
    )

    def fail_if_deserialized(*args, **kwargs):
        raise AssertionError("joblib.load must not run before identity verification")

    monkeypatch.setattr(model_loader.joblib, "load", fail_if_deserialized)

    loader = model_loader.ModelLoader(
        model_path=model_path,
        preprocessor_path=preprocessor_path,
        feature_columns_path=feature_columns_path,
    )
    with pytest.raises(model_loader.ModelArtifactError, match="identity verification failed"):
        loader.load()
