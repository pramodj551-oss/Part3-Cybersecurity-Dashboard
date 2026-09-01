"""Regression model performance page."""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from config.config import EVALUATION_REPORT, METRICS_OUTPUT


def _load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _load_metrics():
    """Load Part 2 metrics from either the evaluation report or metrics JSON."""
    candidates = [Path(EVALUATION_REPORT), Path(METRICS_OUTPUT)]
    for candidate in candidates:
        if not candidate.is_file() or candidate.stat().st_size == 0:
            continue
        payload = _load_json(candidate)
        if isinstance(payload, dict):
            nested = payload.get("metrics")
            if isinstance(nested, dict):
                return nested
            return payload
        if isinstance(payload, list):
            rows = {
                str(item["Metric"]): item["Value"]
                for item in payload
                if isinstance(item, dict) and "Metric" in item and "Value" in item
            }
            if rows:
                return rows
    raise FileNotFoundError("No usable regression metrics JSON artifact is available.")


def _normalize(metrics):
    aliases = {
        "MAE": ["MAE", "mae", "mean_absolute_error"],
        "RMSE": ["RMSE", "rmse", "root_mean_squared_error"],
        "R²": ["R2", "R²", "R2 Score", "r2", "r_squared"],
    }
    result = {}
    for label, keys in aliases.items():
        for key in keys:
            if key in metrics:
                try:
                    value = float(metrics[key])
                except (TypeError, ValueError):
                    continue
                if pd.notna(value):
                    result[label] = value
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
        columns[index].metric(
            label,
            "N/A" if label not in metrics else f"{metrics[label]:.4f}",
        )

    df = pd.DataFrame({"Metric": list(metrics), "Value": list(metrics.values())})
    if not df.empty:
        st.plotly_chart(
            px.bar(df, x="Metric", y="Value", title="Regression Metrics"),
            use_container_width=True,
        )
        st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    render()
