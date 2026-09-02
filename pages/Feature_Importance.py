"""Feature Importance page with Part 2 artifact normalization."""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from config.config import FEATURE_IMPORTANCE_OUTPUT
from src.explainability import ExplainabilityError


def _load_importance(path: Path) -> pd.DataFrame:
    """Load and validate the machine-readable STEP 20 contract."""
    if not path.is_file():
        raise FileNotFoundError("Feature importance artifact is not available.")

    df = pd.read_csv(path).rename(columns={"feature": "Feature", "importance": "Importance"})
    required = {"Feature", "Importance"}
    if not required.issubset(df.columns):
        raise ExplainabilityError("Expected feature/importance columns.")

    df["Importance"] = pd.to_numeric(df["Importance"], errors="coerce")
    df = df.dropna(subset=["Importance"])
    if df.empty:
        raise ExplainabilityError("Feature importance data is empty.")
    if not np.isfinite(df["Importance"].to_numpy(dtype=float)).all():
        raise ExplainabilityError("Feature importance contains non-finite values.")
    return df


def render():
    st.title("⭐ Feature Importance")
    try:
        df = _load_importance(Path(FEATURE_IMPORTANCE_OUTPUT))
    except FileNotFoundError:
        st.warning("Feature importance artifact is not available yet.")
        return
    except (OSError, ValueError, ExplainabilityError):
        st.error("Unable to load feature importance data safely.")
        return

    top_n = st.slider("Number of Features", 1, len(df), min(10, len(df)))
    display = df.sort_values(["Importance", "Feature"], ascending=[False, True], kind="mergesort").head(top_n)
    fig = px.bar(display, x="Importance", y="Feature", orientation="h", title="Top Feature Importance")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, width="stretch")
    st.dataframe(display, width="stretch")


if __name__ == "__main__":
    render()
