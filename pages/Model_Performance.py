"""Regression model performance page."""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from config.config import EVALUATION_REPORT, METRICS_OUTPUT


def _load_metrics():
    for candidate in [Path(EVALUATION_REPORT), Path(METRICS_OUTPUT)]:
        if candidate.is_file():
            with candidate.open(encoding="utf-8") as handle:
                payload = json.load(handle)
            if isinstance(payload, dict):
                return payload
    raise FileNotFoundError("No regression metrics JSON artifact is available.")


def _normalize(metrics):
    aliases = {
        "MAE": ["MAE", "mae", "mean_absolute_error"],
        "RMSE": ["RMSE", "rmse", "root_mean_squared_error"],
        "R²": ["R2", "R²", "r2", "r_squared"],
    }
    result = {}
    for label, keys in aliases.items():
        for key in keys:
            if key in metrics:
                result[label] = float(metrics[key])
                break
    return result


def render():
    st.title("📉 Model Performance")
    try:
        metrics = _normalize(_load_metrics())
    except Exception as error:
        st.warning(f"Regression metrics are not available yet: {error}")
        return

    columns = st.columns(3)
    for index, label in enumerate(["MAE", "RMSE", "R²"]):
        columns[index].metric(label, "N/A" if label not in metrics else f"{metrics[label]:.4f}")

    df = pd.DataFrame({"Metric": list(metrics), "Value": list(metrics.values())})
    if not df.empty:
        st.plotly_chart(px.bar(df, x="Metric", y="Value", title="Regression Metrics"), use_container_width=True)
        st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    render()
