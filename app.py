"""AI-Powered Cybersecurity Dashboard entry point."""

import streamlit as st

from config.config import APP_ICON, APP_TITLE, LAYOUT, SIDEBAR_STATE
from src.deployment_fingerprint import get_runtime_commit
from src.runtime_artifact_identity import verify_runtime_artifact_identity

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

st.subheader("Deployment fingerprint")
runtime_commit = get_runtime_commit()
if len(runtime_commit) == 40 and all(c in "0123456789abcdef" for c in runtime_commit.lower()):
    st.code(f"Running Commit: {runtime_commit}")
else:
    st.warning(f"Running Commit: {runtime_commit}")

st.subheader("Runtime artifact identity")
identity_ok, runtime_hashes, identity_message = verify_runtime_artifact_identity()
if identity_ok:
    st.success(f"PASS: {identity_message}")
    with st.expander("Runtime SHA-256 values"):
        for relative, digest in runtime_hashes.items():
            st.code(f"{relative} = {digest}")
else:
    st.error(f"FAIL: {identity_message}")

st.subheader("Available modules")
modules = [
    "Home",
    "Dataset Explorer",
    "EDA Dashboard",
    "Prediction",
    "Feature Importance",
    "Model Performance",
    "Health",
]
for module in modules:
    st.markdown(f"- {module}")

st.info(
    "The `pages/` directory is the authoritative Streamlit multipage UI. "
    "This entry point intentionally contains no duplicate placeholder navigation."
)
