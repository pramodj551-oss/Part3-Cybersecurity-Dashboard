"""Machine-readable production health/readiness page."""

import streamlit as st

from src.health import health_snapshot


st.set_page_config(page_title="Health", page_icon="🩺", layout="wide")

st.title("Production Health")
snapshot = health_snapshot()

if snapshot["status"] == "ready":
    st.success("READY")
else:
    st.error("NOT READY")

st.json(snapshot)
