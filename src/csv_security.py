"""Bounded CSV parsing for untrusted dashboard uploads."""

from __future__ import annotations

import csv
import io
from typing import BinaryIO

import pandas as pd

from config.config import (
    MAX_CSV_CELLS,
    MAX_CSV_COLUMNS,
    MAX_CSV_FIELD_LENGTH,
    MAX_CSV_ROWS,
)


class CSVSecurityError(ValueError):
    """Safe, user-facing error for rejected untrusted CSV input."""


def _quote_is_unterminated(raw: bytes) -> bool:
    """Detect an unclosed CSV quote without exposing parser internals."""
    in_quotes = False
    index = 0
    while index < len(raw):
        if raw[index] == 34:
            if in_quotes and index + 1 < len(raw) and raw[index + 1] == 34:
                index += 2
                continue
            in_quotes = not in_quotes
        index += 1
    return in_quotes


def _safe_reader(stream: BinaryIO):
    """Read CSV records with strict UTF-8 and bounded parser complexity."""
    try:
        raw = stream.read()
        if not isinstance(raw, (bytes, bytearray)):
            raise CSVSecurityError("Unable to read the uploaded CSV.")
        raw = bytes(raw)
        if _quote_is_unterminated(raw):
            raise CSVSecurityError("CSV contains an unterminated quoted field.")
        text = io.TextIOWrapper(
            io.BytesIO(raw), encoding="utf-8-sig", errors="strict", newline=""
        )
    except UnicodeDecodeError as error:
        raise CSVSecurityError("CSV must be valid UTF-8 text.") from error
    except CSVSecurityError:
        raise
    except (OSError, TypeError, ValueError) as error:
        raise CSVSecurityError("Unable to read the uploaded CSV encoding.") from error

    old_limit = csv.field_size_limit()
    # Allow one byte/character beyond the configured field boundary so that
    # header validation gets the first opportunity to classify an oversized
    # column name as an invalid column, rather than as a generic field error.
    parser_limit = MAX_CSV_FIELD_LENGTH + 1
    csv.field_size_limit(parser_limit)
    try:
        reader = csv.reader(text, strict=True)
        rows = []
        total_cells = 0
        for row_number, row in enumerate(reader, start=1):
            if row_number == 1:
                if not row or all(field == "" for field in row):
                    raise CSVSecurityError("CSV header is empty.")
                if len(row) == 0:
                    raise CSVSecurityError("CSV must contain at least one column.")
                if len(row) > MAX_CSV_COLUMNS:
                    raise CSVSecurityError(
                        f"CSV exceeds the maximum of {MAX_CSV_COLUMNS} columns."
                    )
                # Header-specific validation must happen before the generic
                # data-field validation path.
                if any(not name or len(name) > MAX_CSV_FIELD_LENGTH for name in row):
                    raise CSVSecurityError("CSV contains an invalid column name.")
            else:
                if len(row) > MAX_CSV_COLUMNS:
                    raise CSVSecurityError(
                        f"CSV exceeds the maximum of {MAX_CSV_COLUMNS} columns."
                    )
                if row_number > MAX_CSV_ROWS + 1:
                    raise CSVSecurityError(
                        f"CSV exceeds the maximum of {MAX_CSV_ROWS:,} data rows."
                    )
                if any(len(field) > MAX_CSV_FIELD_LENGTH for field in row):
                    raise CSVSecurityError("CSV field exceeds the configured maximum length.")
            total_cells += len(row)
            if total_cells > MAX_CSV_CELLS:
                raise CSVSecurityError("CSV exceeds the configured cell limit.")
            rows.append(row)
    except UnicodeDecodeError as error:
        raise CSVSecurityError("CSV must be valid UTF-8 text.") from error
    except csv.Error as error:
        message = str(error).lower()
        if "field larger than field limit" in message:
            raise CSVSecurityError("CSV field exceeds the configured maximum length.") from error
        raise CSVSecurityError("CSV structure is invalid or malformed.") from error
    except CSVSecurityError:
        raise
    finally:
        csv.field_size_limit(old_limit)
        try:
            text.detach()
        except ValueError:
            pass

    if not rows:
        raise CSVSecurityError("Uploaded CSV is empty.")

    header = rows[0]
    if len(set(header)) != len(header):
        raise CSVSecurityError("CSV contains duplicate column names.")

    expected_columns = len(header)
    for row in rows[1:]:
        if len(row) != expected_columns:
            raise CSVSecurityError("CSV rows have inconsistent column counts.")

    return rows


def read_bounded_csv(uploaded_file) -> pd.DataFrame:
    """Parse an untrusted CSV within configured size and structure limits."""
    if uploaded_file is None:
        raise CSVSecurityError("No CSV file was uploaded.")

    try:
        if isinstance(uploaded_file, (bytes, bytearray)):
            stream = io.BytesIO(bytes(uploaded_file))
        else:
            uploaded_file.seek(0)
            stream = uploaded_file
        rows = _safe_reader(stream)
    except CSVSecurityError:
        raise
    except (OSError, ValueError, TypeError) as error:
        raise CSVSecurityError("Unable to read the uploaded CSV.") from error
    finally:
        if not isinstance(uploaded_file, (bytes, bytearray)):
            try:
                uploaded_file.seek(0)
            except (OSError, ValueError, AttributeError):
                pass

    try:
        return pd.DataFrame(rows[1:], columns=rows[0])
    except (MemoryError, ValueError, TypeError) as error:
        raise CSVSecurityError("CSV could not be converted safely into a table.") from error
