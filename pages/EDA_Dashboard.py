"""
==========================================================
AI-Powered Cybersecurity Dashboard
EDA Dashboard
Version: 3.0
==========================================================
"""

import pandas as pd
import streamlit as st

from config.config import MAX_UPLOAD_SIZE_MB
from src.csv_security import CSVSecurityError, read_bounded_csv
from src.upload_validation import validate_upload_size
from src.visualization import visualizer
from src.arrow_compat import make_display_safe


def render():
    st.title("📈 Exploratory Data Analysis")
    st.markdown(
        """
Explore the uploaded cybersecurity dataset using
interactive visualizations.
"""
    )

    uploaded_file = st.file_uploader(
        "Upload Dataset",
        type=["csv"],
        key="eda_upload"
    )
    if uploaded_file is None:
        st.info("Upload a CSV dataset to begin EDA.")
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
    st.divider()
    visualizer.display_dataset_overview(df)
    st.divider()
    visualizer.display_dataframe(df.head(10))
    st.divider()
    st.subheader("Missing Value Analysis")
    visualizer.plot_missing_values(df)
    st.divider()
    target_column = st.selectbox("Select Target Column", df.columns)
    visualizer.plot_target_distribution(df, target_column)
    st.divider()
    st.subheader("Correlation Analysis")
    visualizer.plot_correlation(df)
    st.divider()
    st.subheader("Descriptive Statistics")
    st.dataframe(make_display_safe(df.describe(include="all")), width="stretch")
    st.divider()
    st.subheader("Dataset Information")
    info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing": df.isnull().sum(),
        "Unique": df.nunique()
    })
    st.dataframe(info, width="stretch")
    st.divider()
    st.success("EDA completed successfully.")


if __name__ == "__main__":
    render()
