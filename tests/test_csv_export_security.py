"""Regression tests for spreadsheet-formula-safe CSV exports."""

import pandas as pd

from src.utils import dataframe_to_safe_csv, export_csv


def test_dataframe_to_safe_csv_neutralizes_formula_prefixes():
    dataframe = pd.DataFrame(
        {
            "payload": ["=1+1", "+SUM(A1)", "-10", "@cmd", "  =1+1", "normal"],
            "number": [1, 2, 3, 4, 5, 6],
        }
    )

    csv_text = dataframe_to_safe_csv(dataframe)
    lines = csv_text.splitlines()

    assert lines[1].startswith("'=1+1,")
    assert lines[2].startswith("'+SUM(A1),")
    assert lines[3].startswith("'-10,")
    assert lines[4].startswith("'@cmd,")
    assert lines[5].startswith("'  =1+1,")
    assert lines[6].startswith("normal,")


def test_dataframe_to_safe_csv_preserves_typed_numeric_values():
    dataframe = pd.DataFrame({"number": [1, -10, 3.5]})

    csv_text = dataframe_to_safe_csv(dataframe)

    assert csv_text.splitlines() == ["number", "1", "-10", "3.5"]


def test_export_csv_uses_safe_serialization(tmp_path):
    output_path = tmp_path / "export.csv"
    dataframe = pd.DataFrame({"value": ["=HYPERLINK(\"https://example.com\")", "safe"]})

    export_csv(dataframe, output_path)

    assert output_path.read_text(encoding="utf-8").splitlines() == [
        "value",
        "'=HYPERLINK(\"https://example.com\")",
        "safe",
    ]
