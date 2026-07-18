"""
==========================================================
AI-Powered Cybersecurity Dashboard
Dataset Explorer Page
Version: 3.0
==========================================================
"""

import streamlit as st
import pandas as pd

from src.visualization import visualizer
from src.utils import dataset_summary


def render():

    st.title("📊 Dataset Explorer")

    st.markdown(
        """
Upload a cybersecurity dataset to explore its structure,
quality, and statistical information.
"""
    )

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"]
    )

    if uploaded_file is None:

        st.info("Please upload a CSV dataset.")

        return

    try:

        df = pd.read_csv(uploaded_file)

    except Exception as error:

        st.error(f"Unable to load dataset.\n\n{error}")

        return

    st.success("Dataset loaded successfully.")

    # ------------------------------------------------------
    # Dataset Summary
    # ------------------------------------------------------

    summary = dataset_summary(df)

    st.subheader("Dataset Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.metric("Rows", summary["Rows"])
        st.metric("Columns", summary["Columns"])

    with col2:

        st.metric(
            "Missing Values",
            summary["Missing Values"]
        )

        st.metric(
            "Duplicate Records",
            summary["Duplicate Records"]
        )

    st.divider()

    # ------------------------------------------------------
    # Dataset Preview
    # ------------------------------------------------------

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    st.divider()

    # ------------------------------------------------------
    # Column Information
    # ------------------------------------------------------

    st.subheader("Column Information")

    info = pd.DataFrame({

        "Column": df.columns,

        "Data Type": df.dtypes.astype(str),

        "Missing Values": df.isnull().sum().values,

        "Unique Values": df.nunique().values

    })

    st.dataframe(
        info,
        use_container_width=True
    )

    st.divider()

    # ------------------------------------------------------
    # Missing Value Visualization
    # ------------------------------------------------------

    visualizer.plot_missing_values(df)

    st.divider()

    # ------------------------------------------------------
    # Raw Dataset Download
    # ------------------------------------------------------

    st.download_button(

        label="Download Dataset",

        data=df.to_csv(index=False),

        file_name="dataset.csv",

        mime="text/csv"

    )


if __name__ == "__main__":

    render()
