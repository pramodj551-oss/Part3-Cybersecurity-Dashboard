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


def _safe_reader(stream: BinaryIO):
    """Read CSV records with strict UTF-8 and bounded parser complexity."""
    try:
        text = io.TextIOWrapper(
            stream, encoding="utf-8-sig", errors="strict", newline=""
        )
    except (TypeError, ValueError) as error:
        raise CSVSecurityError("Unable to read the uploaded CSV encoding.") from error

    old_limit = csv.field_size_limit()
    csv.field_size_limit(MAX_CSV_FIELD_LENGTH)
    try:
        reader = csv.reader(text)
        rows = []
        total_cells = 0
        for row_number, row in enumerate(reader, start=1):
            if row_number == 1 and (not row or all(field == "" for field in row)):
                raise CSVSecurityError("CSV header is empty.")
            if len(row) > MAX_CSV_COLUMNS:
                raise CSVSecurityError(
                    f"CSV exceeds the maximum of {MAX_CSV_COLUMNS} columns."
                )
            if row_number > MAX_CSV_ROWS + 1:
                raise CSVSecurityError(
                    f"CSV exceeds the maximum of {MAX_CSV_ROWS:,} data rows."
                )
            if any(len(field) > MAX_CSV_FIELD_LENGTH for field in row):
                raise CSVSecurityError(
                    "CSV field exceeds the configured maximum length."
                )
            total_cells += len(row)
            if total_cells > MAX_CSV_CELLS:
                raise CSVSecurityError("CSV exceeds the configured cell limit.")
            rows.append(row)
    except UnicodeDecodeError as error:
        raise CSVSecurityError("CSV must be valid UTF-8 text.") from error
    except csv.Error as error:
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
    if len(header) == 0:
        raise CSVSecurityError("CSV must contain at least one column.")
    if len(set(header)) != len(header):
        raise CSVSecurityError("CSV contains duplicate column names.")
    if any(not name or len(name) > MAX_CSV_FIELD_LENGTH for name in header):
        raise CSVSecurityError("CSV contains an invalid column name.")

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
        uploaded_file.seek(0)
        rows = _safe_reader(uploaded_file)
    except CSVSecurityError:
        raise
    except (OSError, ValueError, TypeError) as error:
        raise CSVSecurityError("Unable to read the uploaded CSV.") from error
    finally:
        try:
            uploaded_file.seek(0)
        except (OSError, ValueError, AttributeError):
            pass

    try:
        return pd.DataFrame(rows[1:], columns=rows[0])
    except (MemoryError, ValueError, TypeError) as error:
        raise CSVSecurityError("CSV could not be converted safely into a table.") from error
