"""Streamlit dataframe display compatibility helpers."""

import pandas as pd


def make_display_safe(df: pd.DataFrame) -> pd.DataFrame:
    """Return a display-only copy with mixed object columns normalized to strings.

    Uploaded CSVs can contain mixed values such as numeric IDs and values like
    ``INC-00001`` in the same column. PyArrow may reject those object columns
    during Streamlit dataframe serialization. This helper affects only the
    display copy; the original dataframe used by analytics and prediction is
    unchanged.
    """
    display = df.copy()

    for column in display.select_dtypes(include=["object"]).columns:
        display[column] = display[column].astype("string")

    return display
