"""AI-Powered Cybersecurity Dashboard entry point."""

import streamlit as st

from config.config import APP_ICON, APP_TITLE, LAYOUT, SIDEBAR_STATE

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE,
)

st.title(f"{APP_ICON} {APP_TITLE}")
st.markdown(
    """
Use the pages in the sidebar to explore cybersecurity incidents, run EDA,
inspect model artifacts, and generate severity-score predictions.

**Runtime note:** prediction requires the Part 2 artifacts
`models/best_model.pkl`, `models/preprocessor.pkl`, and
`models/feature_columns.pkl`. The dashboard never fabricates missing model
artifacts; it reports a clear error instead.
"""
)

st.divider()

col1, col2, col3 = st.columns(3)
col1.metric("Problem", "Severity-score regression")
col2.metric("Framework", "Streamlit")
col3.metric("Version", "3.0")

st.subheader("Available modules")
modules = [
    "Home",
    "Dataset Explorer",
    "EDA Dashboard",
    "Prediction",
    "Feature Importance",
    "Model Performance",
]
for module in modules:
    st.markdown(f"- {module}")

st.info(
    "The `pages/` directory is the authoritative Streamlit multipage UI. "
    "This entry point intentionally contains no duplicate placeholder navigation."
)
