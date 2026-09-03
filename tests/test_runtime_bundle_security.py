"""Adversarial tests for Part 2 runtime bundle extraction."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from src.runtime_bundle_security import (
    EXPECTED_BUNDLE_MEMBERS,
    safe_extract_runtime_bundle,
    validate_runtime_bundle,
)


def _write_bundle(path: Path, names: list[str]) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        for name in names:
            zf.writestr(name, b"test")


def test_safe_bundle_extracts(tmp_path: Path) -> None:
    archive = tmp_path / "runtime.zip"
    _write_bundle(archive, sorted(EXPECTED_BUNDLE_MEMBERS))
    destination = tmp_path / "out"

    safe_extract_runtime_bundle(archive, destination)

    assert sorted(p.relative_to(destination).as_posix() for p in destination.rglob("*")) == sorted(EXPECTED_BUNDLE_MEMBERS)


def test_parent_traversal_is_rejected_before_extraction(tmp_path: Path) -> None:
    archive = tmp_path / "runtime.zip"
    names = sorted(EXPECTED_BUNDLE_MEMBERS - {"outputs/metrics.json"}) + ["../escaped.txt"]
    _write_bundle(archive, names)

    with pytest.raises(ValueError, match="member contract|Unsafe ZIP member path"):
        validate_runtime_bundle(archive)
    assert not (tmp_path / "escaped.txt").exists()


def test_absolute_path_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "runtime.zip"
    names = sorted(EXPECTED_BUNDLE_MEMBERS - {"outputs/metrics.json"}) + ["/tmp/escaped.txt"]
    _write_bundle(archive, names)

    with pytest.raises(ValueError):
        validate_runtime_bundle(archive)


def test_backslash_path_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "runtime.zip"
    names = sorted(EXPECTED_BUNDLE_MEMBERS - {"outputs/metrics.json"}) + ["models\\evil.pkl"]
    _write_bundle(archive, names)

    with pytest.raises(ValueError):
        validate_runtime_bundle(archive)


def test_unexpected_member_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "runtime.zip"
    names = sorted(EXPECTED_BUNDLE_MEMBERS) + ["unexpected.txt"]
    _write_bundle(archive, names)

    with pytest.raises(ValueError, match="contract mismatch"):
        validate_runtime_bundle(archive)


def test_duplicate_member_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "runtime.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        for name in sorted(EXPECTED_BUNDLE_MEMBERS):
            zf.writestr(name, b"test")
        zf.writestr("models/best_model.pkl", b"duplicate")

    with pytest.raises(ValueError, match="duplicate"):
        validate_runtime_bundle(archive)
