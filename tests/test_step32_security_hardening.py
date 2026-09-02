"""Dedicated STEP 32 regression tests for security hardening fixes."""

from pathlib import Path

import pytest

from src.csv_security import CSVSecurityError
from src.utils import load_dataset


def test_utils_load_dataset_uses_bounded_csv_parser(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("src.utils.DATA_DIR", tmp_path)
    path = tmp_path / "dataset.csv"
    path.write_bytes(b"a,b\n1,2\n")

    frame = load_dataset(path)

    assert list(frame.columns) == ["a", "b"]
    assert frame.shape == (1, 2)


def test_utils_load_dataset_rejects_oversized_file(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("src.utils.DATA_DIR", tmp_path)
    monkeypatch.setattr("src.utils.MAX_UPLOAD_SIZE_MB", 1)
    path = tmp_path / "dataset.csv"
    path.write_bytes(b"a\n" + b"1" * (1024 * 1024) + b"\n")

    with pytest.raises(ValueError, match="maximum allowed size"):
        load_dataset(path)


def test_utils_load_dataset_preserves_csv_security_errors(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("src.utils.DATA_DIR", tmp_path)
    path = tmp_path / "dataset.csv"
    path.write_bytes(b"a,a\n1,2\n")

    with pytest.raises(CSVSecurityError, match="duplicate column"):
        load_dataset(path)
