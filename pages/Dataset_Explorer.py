"""
==========================================================
AI-Powered Cybersecurity Dashboard
Dataset Explorer Page
Version: 3.0
==========================================================
"""

import pandas as pd
import streamlit as st

from config.config import MAX_UPLOAD_SIZE_MB
from src.csv_security import CSVSecurityError, read_bounded_csv
from src.upload_validation import validate_upload_size
from src.visualization import visualizer
from src.utils import dataset_summary
from src.arrow_compat import make_display_safe


def render():
    st.title("📊 Dataset Explorer")
    st.markdown(
        """
Upload a cybersecurity dataset to explore its structure,
quality, and statistical information.
"""
    )

    uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])
    if uploaded_file is None:
        st.info("Please upload a CSV dataset.")
        return

    try:
        validate_upload_size(uploaded_file, MAX_UPLOAD_SIZE_MB)
        df = read_bounded_csv(uploaded_file)
    except ValueError as error:
        st.error(str(error))
        return
    except CSVSecurityError as error:
        st.error(str(error))
        return

    st.success("Dataset loaded successfully.")

    summary = dataset_summary(df)
    st.subheader("Dataset Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Rows", summary["Rows"])
        st.metric("Columns", summary["Columns"])
    with col2:
        st.metric("Missing Values", summary["Missing Values"])
        st.metric("Duplicate Records", summary["Duplicate Records"])

    st.divider()
    st.subheader("Dataset Preview")
    st.dataframe(make_display_safe(df.head(20)), width="stretch")
    st.divider()

    st.subheader("Column Information")
    info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })
    st.dataframe(info, width="stretch")
    st.divider()

    visualizer.plot_missing_values(df)
    st.divider()
    st.download_button(
        label="Download Dataset",
        data=df.to_csv(index=False),
        file_name="dataset.csv",
        mime="text/csv"
    )


if __name__ == "__main__":
    render()
