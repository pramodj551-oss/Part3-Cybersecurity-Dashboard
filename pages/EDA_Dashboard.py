"""
==========================================================
AI-Powered Cybersecurity Dashboard
EDA Dashboard
Version: 3.0
==========================================================
"""

import streamlit as st
import pandas as pd

from src.visualization import visualizer


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

        df = pd.read_csv(uploaded_file)

    except Exception as error:

        st.error(f"Unable to load dataset.\n\n{error}")

        return

    st.success("Dataset loaded successfully.")

    st.divider()

    # ------------------------------------------------------
    # Dataset Overview
    # ------------------------------------------------------

    visualizer.display_dataset_overview(df)

    st.divider()

    # ------------------------------------------------------
    # Dataset Preview
    # ------------------------------------------------------

    visualizer.display_dataframe(df.head(10))

    st.divider()

    # ------------------------------------------------------
    # Missing Value Analysis
    # ------------------------------------------------------

    st.subheader("Missing Value Analysis")

    visualizer.plot_missing_values(df)

    st.divider()

    # ------------------------------------------------------
    # Target Distribution
    # ------------------------------------------------------

    target_column = st.selectbox(
        "Select Target Column",
        df.columns
    )

    visualizer.plot_target_distribution(
        df,
        target_column
    )

    st.divider()

    # ------------------------------------------------------
    # Correlation Heatmap
    # ------------------------------------------------------

    st.subheader("Correlation Analysis")

    visualizer.plot_correlation(df)

    st.divider()

    # ------------------------------------------------------
    # Numerical Summary
    # ------------------------------------------------------

    st.subheader("Descriptive Statistics")

    st.dataframe(
        df.describe(include="all"),
        use_container_width=True
    )

    st.divider()

    # ------------------------------------------------------
    # Data Types
    # ------------------------------------------------------

    st.subheader("Dataset Information")

    info = pd.DataFrame({

        "Column": df.columns,

        "Data Type": df.dtypes.astype(str),

        "Missing": df.isnull().sum(),

        "Unique": df.nunique()

    })

    st.dataframe(
        info,
        use_container_width=True
    )

    st.divider()

    st.success(
        "EDA completed successfully."
    )


if __name__ == "__main__":

    render()
