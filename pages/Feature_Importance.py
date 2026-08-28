"""Feature Importance page with Part 2 artifact normalization."""

from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from config.config import FEATURE_IMPORTANCE_OUTPUT


def render():
    st.title("⭐ Feature Importance")
    path = Path(FEATURE_IMPORTANCE_OUTPUT)
    if not path.is_file():
        st.warning("Feature importance artifact is not available yet.")
        return
    try:
        df = pd.read_csv(path)
        df = df.rename(columns={"feature": "Feature", "importance": "Importance"})
        required = {"Feature", "Importance"}
        if not required.issubset(df.columns):
            raise ValueError("Expected feature/importance columns.")
        df["Importance"] = pd.to_numeric(df["Importance"], errors="coerce")
        df = df.dropna(subset=["Importance"])
    except Exception as error:
        st.error(f"Unable to load feature importance data: {error}")
        return
    if df.empty:
        st.warning("Feature importance data is empty.")
        return
    top_n = st.slider("Number of Features", 1, len(df), min(10, len(df)))
    display = df.sort_values("Importance", ascending=False).head(top_n)
    fig = px.bar(display, x="Importance", y="Feature", orientation="h", title="Top Feature Importance")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(display, use_container_width=True)


if __name__ == "__main__":
    render()
