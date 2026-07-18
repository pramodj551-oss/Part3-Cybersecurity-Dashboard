"""
==========================================================
AI-Powered Cybersecurity Dashboard
Main Streamlit Application
Version: 3.0
==========================================================
"""

import streamlit as st

from config.config import (
    APP_TITLE,
    APP_ICON,
    LAYOUT,
    SIDEBAR_STATE
)

# ==========================================================
# Streamlit Page Configuration
# ==========================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE
)

# ==========================================================
# Session State Initialization
# ==========================================================

if "dashboard_loaded" not in st.session_state:
    st.session_state.dashboard_loaded = True

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# ==========================================================
# Header
# ==========================================================

st.title("🛡️ AI-Powered Cybersecurity Dashboard")

st.markdown(
    """
Welcome to the **AI-Powered Cybersecurity Dashboard**.

This dashboard provides an interactive interface for exploring
cybersecurity incidents, visualizing datasets, evaluating
machine learning models, and predicting incident severity.
"""
)

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("Navigation")

selected_page = st.sidebar.radio(
    "Choose a Dashboard Module",
    (
        "🏠 Home",
        "📊 Dataset Explorer",
        "📈 EDA Dashboard",
        "🤖 Prediction",
        "⭐ Feature Importance",
        "📉 Model Performance"
    )
)

# ==========================================================
# Home
# ==========================================================

if selected_page == "🏠 Home":

    st.header("Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Project", "Cybersecurity ML")

    col2.metric("Model", "Random Forest")

    col3.metric("Version", "3.0")

    st.success("Dashboard initialized successfully.")

    st.markdown("---")

    st.subheader("Features")

    st.markdown(
        """
- Dataset Exploration
- Interactive Visualizations
- Machine Learning Predictions
- Feature Importance Analysis
- Model Performance Metrics
- Export Prediction Results
"""
    )

# ==========================================================
# Placeholder Pages
# ==========================================================

elif selected_page == "📊 Dataset Explorer":

    st.header("Dataset Explorer")
    st.info("Module under development.")

elif selected_page == "📈 EDA Dashboard":

    st.header("EDA Dashboard")
    st.info("Module under development.")

elif selected_page == "🤖 Prediction":

    st.header("Prediction")
    st.info("Module under development.")

elif selected_page == "⭐ Feature Importance":

    st.header("Feature Importance")
    st.info("Module under development.")

elif selected_page == "📉 Model Performance":

    st.header("Model Performance")
    st.info("Module under development.")

# ==========================================================
# Footer
# ==========================================================

st.markdown("---")

st.caption(
    "AI-Powered Cybersecurity Dashboard | Version 3.0 | "
    "Developed using Streamlit"
  )
