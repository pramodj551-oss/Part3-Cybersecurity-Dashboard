"""
==========================================================
AI-Powered Cybersecurity Dashboard
Model Performance Page
Version: 3.0
==========================================================
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from config.config import EVALUATION_REPORT


def render():

    st.title("📉 Model Performance")

    st.markdown(
        """
Review the performance of the trained machine learning model
using standard classification metrics.
        """
    )

    report_file = Path(EVALUATION_REPORT)

    if not report_file.exists():

        st.warning(
            "Evaluation report not found.\n"
            "Run the model evaluation pipeline first."
        )

        return

    try:

        report_df = pd.read_csv(report_file)

    except Exception as error:

        st.error(f"Unable to load evaluation report.\n\n{error}")

        return

    st.success("Evaluation report loaded successfully.")

    st.divider()

    # ------------------------------------------------------
    # Performance Metrics
    # ------------------------------------------------------

    required_metrics = [
        "Accuracy",
        "Precision",
        "Recall",
        "F1-Score"
    ]

    available_metrics = {
        row["Metric"]: row["Value"]
        for _, row in report_df.iterrows()
        if "Metric" in report_df.columns and "Value" in report_df.columns
    }

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Accuracy",
            f"{available_metrics.get('Accuracy', 0):.4f}"
        )

        st.metric(
            "Precision",
            f"{available_metrics.get('Precision', 0):.4f}"
        )

    with col2:

        st.metric(
            "Recall",
            f"{available_metrics.get('Recall', 0):.4f}"
        )

        st.metric(
            "F1-Score",
            f"{available_metrics.get('F1-Score', 0):.4f}"
        )

    st.divider()

    # ------------------------------------------------------
    # Metrics Visualization
    # ------------------------------------------------------

    if (
        "Metric" in report_df.columns
        and "Value" in report_df.columns
    ):

        metric_df = report_df[
            report_df["Metric"].isin(required_metrics)
        ]

        fig = px.bar(

            metric_df,

            x="Metric",

            y="Value",

            color="Metric",

            title="Model Performance Metrics"

        )

        fig.update_layout(showlegend=False)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ------------------------------------------------------
    # Complete Evaluation Report
    # ------------------------------------------------------

    st.subheader("Evaluation Report")

    st.dataframe(
        report_df,
        use_container_width=True
    )

    st.divider()

    # ------------------------------------------------------
    # Download
    # ------------------------------------------------------

    st.download_button(

        label="Download Evaluation Report",

        data=report_df.to_csv(index=False),

        file_name="evaluation_report.csv",

        mime="text/csv"

    )

    st.success(
        "Model performance analysis completed successfully."
    )


if __name__ == "__main__":

    render()
