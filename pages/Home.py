"""
==========================================================
AI-Powered Cybersecurity Dashboard
Home Page
Version: 3.0
==========================================================
"""

import streamlit as st

from config.config import APP_TITLE


def render():

    st.title("🛡️ AI-Powered Cybersecurity Dashboard")

    st.markdown(
        """
Welcome to the **AI-Powered Cybersecurity Dashboard**.

This dashboard provides an interactive interface for:

- Cybersecurity Dataset Exploration
- Exploratory Data Analysis (EDA)
- Machine Learning Prediction
- Feature Importance Analysis
- Model Performance Evaluation

The application is built using a production-ready modular
machine learning architecture.
"""
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Dashboard",
            "Ready"
        )

    with col2:
        st.metric(
            "Model",
            "Random Forest"
        )

    with col3:
        st.metric(
            "Version",
            "3.0"
        )

    st.divider()

    st.subheader("Project Workflow")

    st.markdown(
        """
1. Upload or Load Dataset
2. Explore Dataset
3. Perform Exploratory Data Analysis
4. Generate Predictions
5. Analyze Feature Importance
6. Evaluate Model Performance
"""
    )

    st.divider()

    st.info(
        "Use the navigation menu on the left to explore different dashboard modules."
    )

    st.caption(
        f"{APP_TITLE} | Production Ready Dashboard"
    )


if __name__ == "__main__":

    render()
