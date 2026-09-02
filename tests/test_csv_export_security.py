"""Regression tests for spreadsheet-formula-safe CSV exports."""

import csv
from io import StringIO

import pandas as pd

from src.utils import dataframe_to_safe_csv, export_csv


def _read_csv_rows(csv_text):
    return list(csv.reader(StringIO(csv_text)))


def test_dataframe_to_safe_csv_neutralizes_formula_prefixes():
    dataframe = pd.DataFrame(
        {
            "payload": ["=1+1", "+SUM(A1)", "-10", "@cmd", "  =1+1", "normal"],
            "number": [1, 2, 3, 4, 5, 6],
        }
    )

    rows = _read_csv_rows(dataframe_to_safe_csv(dataframe))
    payloads = [row[0] for row in rows[1:]]

    assert payloads == ["'=1+1", "'+SUM(A1)", "'-10", "'@cmd", "'  =1+1", "normal"]


def test_dataframe_to_safe_csv_preserves_typed_numeric_values():
    dataframe = pd.DataFrame({"number": [1, -10, 3.5]})

    csv_text = dataframe_to_safe_csv(dataframe)
    rows = _read_csv_rows(csv_text)

    assert rows[0] == ["number"]
    assert [float(row[0]) for row in rows[1:]] == [1.0, -10.0, 3.5]
    assert dataframe["number"].dtype == pd.Series([1, -10, 3.5]).dtype


def test_export_csv_uses_safe_serialization(tmp_path):
    output_path = tmp_path / "export.csv"
    dataframe = pd.DataFrame({"value": ["=HYPERLINK(\"https://example.com\")", "safe"]})

    export_csv(dataframe, output_path)

    rows = _read_csv_rows(output_path.read_text(encoding="utf-8"))
    assert rows == [
        ["value"],
        ["'=HYPERLINK(\"https://example.com\")"],
        ["safe"],
    ]
