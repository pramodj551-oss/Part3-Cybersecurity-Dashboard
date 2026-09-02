"""
==========================================================
AI-Powered Cybersecurity Dashboard
Utility Functions
Version: 3.0
==========================================================
"""

from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st

from config.config import DATA_DIR, MAX_UPLOAD_SIZE_MB
from src.csv_security import read_bounded_csv


# ==========================================================
# File Utilities
# ==========================================================

def file_exists(file_path) -> bool:
    """
    Check whether a file exists.
    """

    return Path(file_path).exists()


def create_directory(directory):
    """
    Create directory if it does not exist.
    """

    Path(directory).mkdir(
        parents=True,
        exist_ok=True
    )


# ==========================================================
# Dataset Utilities
# ==========================================================

def load_dataset(file_path):
    """
    Load a local CSV through the bounded parser used for untrusted uploads.

    Dataset loading is restricted to DATA_DIR after canonical path resolution.
    Resolving before the boundary check also prevents symlinks from escaping
    the approved dataset root.
    """

    dataset_root = Path(DATA_DIR).resolve()
    path = Path(file_path).resolve()

    if not path.is_relative_to(dataset_root):
        raise ValueError("Dataset path must be inside the configured data directory.")

    if not path.is_file():
        raise FileNotFoundError("Dataset not found.")
    if path.stat().st_size == 0:
        raise ValueError("Dataset is empty.")
    max_bytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if path.stat().st_size > max_bytes:
        raise ValueError(
            f"Dataset exceeds the maximum allowed size of {MAX_UPLOAD_SIZE_MB} MB."
        )

    with path.open("rb") as handle:
        return read_bounded_csv(handle)


def dataset_summary(df: pd.DataFrame) -> dict:
    """
    Generate basic dataset summary.
    """

    return {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Records": int(df.duplicated().sum())
    }


# ==========================================================
# Export Utilities
# ==========================================================

_CSV_FORMULA_PREFIXES = ("=", "+", "-", "@")


def _sanitize_csv_cell(value):
    """
    Neutralize spreadsheet formula prefixes without changing numeric cells.

    CSV files are plain text, but spreadsheet applications may interpret
    string cells beginning with formula-like characters as executable
    formulas when the file is opened. Prefixing such string values with a
    single quote keeps the displayed value while preventing formula parsing.
    """

    if not isinstance(value, str):
        return value

    stripped = value.lstrip()
    if stripped.startswith(_CSV_FORMULA_PREFIXES):
        return "'" + value

    return value


def dataframe_to_safe_csv(dataframe: pd.DataFrame) -> str:
    """
    Serialize a dataframe to CSV with spreadsheet-formula injection hardening.

    Only string cells are sanitized; numeric and other typed values remain
    unchanged. This helper is for exports/downloads and must not be used for
    model input parsing.
    """

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas DataFrame.")

    safe_dataframe = dataframe.copy()
    for column in safe_dataframe.columns:
        safe_dataframe[column] = safe_dataframe[column].map(_sanitize_csv_cell)

    return safe_dataframe.to_csv(index=False)


def export_csv(
    dataframe: pd.DataFrame,
    output_path
):
    """
    Export dataframe to CSV with spreadsheet-formula injection hardening.
    """

    output_path = Path(output_path)
    output_path.write_text(
        dataframe_to_safe_csv(dataframe),
        encoding="utf-8"
    )


# ==========================================================
# Streamlit Utilities
# ==========================================================

def show_success(message: str):
    st.success(message)


def show_warning(message: str):
    st.warning(message)


def show_error(message: str):
    st.error(message)


def show_info(message: str):
    st.info(message)


# ==========================================================
# Dashboard Information
# ==========================================================

def dashboard_information():

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        """
### Dashboard Information

**Application**

AI-Powered Cybersecurity Dashboard

**Version**

3.0

**Framework**

Streamlit

**Machine Learning**

Severity-score regression
"""
    )


# ==========================================================
# Footer
# ==========================================================

def display_footer():

    st.markdown("---")

    st.caption(
        f"© {datetime.now().year} "
        "AI-Powered Cybersecurity Dashboard"
    )


# ==========================================================
# Download Utility
# ==========================================================

def download_dataframe(
    dataframe: pd.DataFrame,
    filename="prediction_results.csv"
):
    """
    Create a Streamlit download button with CSV formula-injection hardening.
    """

    csv = dataframe_to_safe_csv(dataframe)

    st.download_button(
        label="Download Results",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )


# ==========================================================
# End of Module
# ==========================================================
