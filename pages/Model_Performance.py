"""Model Performance page."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from config.config import EVALUATION_REPORT


def render():
    st.title("📉 Model Performance")
    report_file = Path(EVALUATION_REPORT)

    if not report_file.is_file():
        st.warning(
            "Evaluation report is not available yet. Run the evaluation pipeline "
            f"to generate: {report_file.name}"
        )
        return

    try:
        report_df = pd.read_csv(report_file)
    except Exception as error:
        st.error(f"Unable to load evaluation report: {error}")
        return

    required_columns = {"Metric", "Value"}
    if not required_columns.issubset(report_df.columns):
        st.error("Evaluation report CSV must contain Metric and Value columns.")
        return

    report_df["Value"] = pd.to_numeric(report_df["Value"], errors="coerce")
    available_metrics = dict(zip(report_df["Metric"], report_df["Value"]))
    metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]

    columns = st.columns(2)
    for index, metric in enumerate(metrics):
        value = available_metrics.get(metric)
        with columns[index % 2]:
            st.metric(metric, "N/A" if pd.isna(value) else f"{value:.4f}")

    metric_df = report_df[report_df["Metric"].isin(metrics)].dropna(
        subset=["Value"]
    )
    if not metric_df.empty:
        fig = px.bar(
            metric_df,
            x="Metric",
            y="Value",
            color="Metric",
            title="Model Performance Metrics",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(report_df, use_container_width=True)
    st.download_button(
        label="Download Evaluation Report",
        data=report_df.to_csv(index=False),
        file_name="evaluation_report.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    render()
