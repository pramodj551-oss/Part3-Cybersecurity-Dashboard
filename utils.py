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
    Load dataset from CSV.
    """

    if not file_exists(file_path):
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


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

def export_csv(
    dataframe: pd.DataFrame,
    output_path
):
    """
    Export dataframe to CSV.
    """

    dataframe.to_csv(
        output_path,
        index=False
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

Random Forest Classifier
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
    Create a Streamlit download button.
    """

    csv = dataframe.to_csv(index=False)

    st.download_button(
        label="Download Results",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )


# ==========================================================
# End of Module
# ==========================================================
