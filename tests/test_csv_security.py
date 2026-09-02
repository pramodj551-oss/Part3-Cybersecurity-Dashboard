"""STEP 31-B adversarial tests for untrusted CSV parsing."""

import io

import pandas as pd
import pytest

from config.config import (
    MAX_CSV_CELLS,
    MAX_CSV_COLUMNS,
    MAX_CSV_FIELD_LENGTH,
    MAX_CSV_ROWS,
)
from src.csv_security import CSVSecurityError, read_bounded_csv
from src.upload_validation import validate_upload_size


class Upload(io.BytesIO):
    @property
    def size(self):
        return len(self.getbuffer())


def csv_bytes(payload: bytes):
    return Upload(payload)


def test_zero_byte_upload_is_rejected_before_parser():
    with pytest.raises(ValueError, match="empty"):
        validate_upload_size(csv_bytes(b""), 100)


def test_invalid_upload_size_is_rejected():
    with pytest.raises(ValueError, match="invalid"):
        validate_upload_size(type("Upload", (), {"size": -1})(), 100)


def test_bom_is_accepted_and_removed_from_first_column():
    result = read_bounded_csv(csv_bytes(b"\xef\xbb\xbfa,b\n1,2\n"))
    assert list(result.columns) == ["a", "b"]


def test_invalid_utf8_is_rejected_without_raw_decode_error():
    with pytest.raises(CSVSecurityError, match="valid UTF-8"):
        read_bounded_csv(csv_bytes(b"a,b\n\xff,2\n"))


def test_broken_quoting_is_rejected_or_not_sent_to_prediction():
    with pytest.raises(CSVSecurityError):
        read_bounded_csv(csv_bytes(b"a,b\n1,\"unterminated\n"))


def test_inconsistent_columns_are_rejected():
    with pytest.raises(CSVSecurityError, match="inconsistent"):
        read_bounded_csv(csv_bytes(b"a,b\n1,2,3\n"))


def test_truncated_quoted_record_is_rejected():
    with pytest.raises(CSVSecurityError):
        read_bounded_csv(csv_bytes(b"a,b\n1,\"truncated"))


def test_zero_column_csv_is_rejected():
    with pytest.raises(CSVSecurityError):
        read_bounded_csv(csv_bytes(b"\n"))


def test_header_only_csv_is_allowed_as_empty_dataframe_then_prediction_rejects():
    result = read_bounded_csv(csv_bytes(b"a,b\n"))
    assert isinstance(result, pd.DataFrame)
    assert result.empty


def test_duplicate_columns_are_rejected():
    with pytest.raises(CSVSecurityError, match="duplicate"):
        read_bounded_csv(csv_bytes(b"a,a\n1,2\n"))


def test_empty_column_name_is_rejected():
    with pytest.raises(CSVSecurityError, match="invalid column"):
        read_bounded_csv(csv_bytes(b"a,\n1,2\n"))


def test_extremely_long_column_name_is_rejected(monkeypatch):
    monkeypatch.setattr("src.csv_security.MAX_CSV_FIELD_LENGTH", 16)
    payload = ("a" * 17 + ",b\n1,2\n").encode()
    with pytest.raises(CSVSecurityError, match="invalid column"):
        read_bounded_csv(csv_bytes(payload))


def test_huge_field_is_rejected(monkeypatch):
    monkeypatch.setattr("src.csv_security.MAX_CSV_FIELD_LENGTH", 16)
    payload = ("a,b\n" + "x" * 17 + ",1\n").encode()
    with pytest.raises(CSVSecurityError, match="field"):
        read_bounded_csv(csv_bytes(payload))


def test_excessive_columns_are_rejected(monkeypatch):
    monkeypatch.setattr("src.csv_security.MAX_CSV_COLUMNS", 3)
    payload = b"a,b,c,d\n1,2,3,4\n"
    with pytest.raises(CSVSecurityError, match="columns"):
        read_bounded_csv(csv_bytes(payload))


def test_excessive_rows_are_rejected(monkeypatch):
    monkeypatch.setattr("src.csv_security.MAX_CSV_ROWS", 2)
    payload = b"a\n1\n2\n3\n"
    with pytest.raises(CSVSecurityError, match="data rows"):
        read_bounded_csv(csv_bytes(payload))


def test_excessive_cells_are_rejected(monkeypatch):
    monkeypatch.setattr("src.csv_security.MAX_CSV_CELLS", 5)
    payload = b"a,b,c\n1,2,3\n4,5,6\n"
    with pytest.raises(CSVSecurityError, match="cell limit"):
        read_bounded_csv(csv_bytes(payload))


def test_unusual_unicode_column_names_are_preserved_safely():
    result = read_bounded_csv("安全,δοκιμή\n1,2\n".encode("utf-8"))
    assert list(result.columns) == ["安全", "δοκιμή"]


def test_required_column_spoofing_does_not_create_required_column():
    result = read_bounded_csv(csv_bytes(b"records_affected ,sector\n1,Energy\n"))
    assert "records_affected" not in result.columns


def test_numeric_payloads_are_left_for_prediction_schema_validation():
    result = read_bounded_csv(csv_bytes(b"records_affected\nNaN\n"))
    assert result.loc[0, "records_affected"] == "NaN"


def test_parser_errors_do_not_leak_paths_or_secrets():
    try:
        read_bounded_csv(csv_bytes(b"a,b\n1,\"broken\n"))
    except CSVSecurityError as error:
        message = str(error)
        assert "/" not in message
        assert "\\" not in message
        assert "API_KEY" not in message
        assert "traceback" not in message.lower()


def test_valid_csv_returns_dataframe_with_bounded_shape():
    result = read_bounded_csv(csv_bytes(b"a,b\n1,2\n3,4\n"))
    assert result.shape == (2, 2)
    assert result.shape[0] <= MAX_CSV_ROWS
    assert result.shape[1] <= MAX_CSV_COLUMNS
    assert result.size <= MAX_CSV_CELLS
