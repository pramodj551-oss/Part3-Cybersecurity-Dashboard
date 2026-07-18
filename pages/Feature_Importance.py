"""
==========================================================
AI-Powered Cybersecurity Dashboard
Feature Importance Page
Version: 3.0
==========================================================
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from config.config import FEATURE_IMPORTANCE_OUTPUT


def render():

    st.title("⭐ Feature Importance")

    st.markdown(
        """
Analyze the contribution of each feature used by the
machine learning model.
        """
    )

    feature_file = Path(FEATURE_IMPORTANCE_OUTPUT)

    if not feature_file.exists():

        st.warning(
            "Feature importance file not found.\n"
            "Please run the ML pipeline first."
        )

        return

    try:

        importance_df = pd.read_csv(feature_file)

    except Exception as error:

        st.error(error)

        return

    if importance_df.empty:

        st.warning("Feature importance data is empty.")

        return

    st.success("Feature importance loaded successfully.")

    st.divider()

    # ------------------------------------------------------
    # Top N Features
    # ------------------------------------------------------

    max_features = len(importance_df)

    top_n = st.slider(
        "Number of Features",
        min_value=5,
        max_value=max_features,
        value=min(10, max_features)
    )

    display_df = (
        importance_df
        .sort_values(
            by="Importance",
            ascending=False
        )
        .head(top_n)
    )

    # ------------------------------------------------------
    # Feature Importance Chart
    # ------------------------------------------------------

    fig = px.bar(

        display_df,

        x="Importance",

        y="Feature",

        orientation="h",

        title="Top Feature Importance"

    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ------------------------------------------------------
    # Feature Table
    # ------------------------------------------------------

    st.subheader("Feature Ranking")

    st.dataframe(
        display_df,
        use_container_width=True
    )

    st.divider()

    # ------------------------------------------------------
    # Download
    # ------------------------------------------------------

    st.download_button(

        label="Download Feature Importance",

        data=display_df.to_csv(index=False),

        file_name="feature_importance.csv",

        mime="text/csv"

    )

    st.success(
        "Feature importance analysis completed."
    )


if __name__ == "__main__":

    render()
