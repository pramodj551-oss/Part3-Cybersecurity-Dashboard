"""Feature Importance page."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from config.config import FEATURE_IMPORTANCE_OUTPUT


def render():
    st.title("⭐ Feature Importance")
    feature_file = Path(FEATURE_IMPORTANCE_OUTPUT)

    if not feature_file.is_file():
        st.warning(
            "Feature importance artifact is not available yet. "
            "Run the training/evaluation pipeline to generate: "
            f"{feature_file.name}"
        )
        return

    try:
        importance_df = pd.read_csv(feature_file)
    except Exception as error:
        st.error(f"Unable to load feature importance data: {error}")
        return

    required_columns = {"Feature", "Importance"}
    if not required_columns.issubset(importance_df.columns):
        st.error(
            "Feature importance CSV must contain Feature and Importance columns."
        )
        return
    if importance_df.empty:
        st.warning("Feature importance data is empty.")
        return

    max_features = len(importance_df)
    min_features = 1 if max_features < 5 else 5
    top_n = st.slider(
        "Number of Features",
        min_value=min_features,
        max_value=max_features,
        value=min(10, max_features),
    )
    display_df = importance_df.sort_values(
        by="Importance", ascending=False
    ).head(top_n)

    fig = px.bar(
        display_df,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top Feature Importance",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(display_df, use_container_width=True)
    st.download_button(
        label="Download Feature Importance",
        data=display_df.to_csv(index=False),
        file_name="feature_importance.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    render()
