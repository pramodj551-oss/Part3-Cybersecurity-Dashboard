"""Executable STEP 31-B security contract tests."""

import io

import pytest

from config.config import (
    MAX_CSV_CELLS,
    MAX_CSV_COLUMNS,
    MAX_CSV_FIELD_LENGTH,
    MAX_CSV_ROWS,
)
from src.csv_security import CSVSecurityError, read_bounded_csv


def test_step31b_bounded_csv_accepts_valid_input():
    frame = read_bounded_csv(io.BytesIO(b"a,b\n1,2\n3,4\n"))
    assert list(frame.columns) == ["a", "b"]
    assert len(frame) == 2


def test_step31b_rejects_malformed_csv():
    with pytest.raises(CSVSecurityError, match="malformed|unterminated"):
        read_bounded_csv(io.BytesIO(b'a,b\n"unterminated,2\n'))


def test_step31b_rejects_duplicate_headers():
    with pytest.raises(CSVSecurityError, match="duplicate column"):
        read_bounded_csv(io.BytesIO(b"a,a\n1,2\n"))


def test_step31b_rejects_column_overflow():
    header = ",".join(f"c{i}" for i in range(MAX_CSV_COLUMNS + 1))
    with pytest.raises(CSVSecurityError, match="columns"):
        read_bounded_csv(io.BytesIO((header + "\n").encode()))


def test_step31b_rejects_row_overflow():
    payload = ("a\n" + "1\n" * (MAX_CSV_ROWS + 1)).encode()
    with pytest.raises(CSVSecurityError, match="data rows"):
        read_bounded_csv(io.BytesIO(payload))


def test_step31b_rejects_field_overflow():
    oversized = "x" * (MAX_CSV_FIELD_LENGTH + 1)
    with pytest.raises(CSVSecurityError, match="field|column"):
        read_bounded_csv(io.BytesIO(("a\n" + oversized + "\n").encode()))


def test_step31b_rejects_cell_overflow(monkeypatch):
    monkeypatch.setattr("src.csv_security.MAX_CSV_CELLS", 3)
    with pytest.raises(CSVSecurityError, match="cell"):
        read_bounded_csv(io.BytesIO(b"a,b\n1,2\n"))


def test_step31b_security_limits_are_positive():
    assert MAX_CSV_ROWS > 0
    assert MAX_CSV_COLUMNS > 0
    assert MAX_CSV_CELLS > 0
    assert MAX_CSV_FIELD_LENGTH > 0
