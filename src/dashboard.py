"""
==========================================================
AI-Powered Cybersecurity Dashboard
Dashboard UI Components
Version: 3.0
==========================================================
"""

import streamlit as st

from src.theme import theme


class DashboardUI:
    """
    Reusable UI components for the dashboard.
    """

    @staticmethod
    def page_header(title: str, description: str = ""):
        """
        Display a consistent page header.
        """

        st.title(f"{theme.APP_ICON} {title}")

        if description:
            st.markdown(description)

        st.divider()

    @staticmethod
    def sidebar_branding():
        """
        Display branding in the sidebar.
        """

        st.sidebar.title(theme.APP_NAME)
        st.sidebar.caption(f"Version {theme.APP_VERSION}")

        st.sidebar.divider()

    @staticmethod
    def metric_row(metrics: dict):
        """
        Display metrics in responsive columns.

        Example:
        metric_row({
            "Accuracy": "95%",
            "Precision": "94%",
            "Recall": "93%"
        })
        """

        columns = st.columns(len(metrics))

        for column, (label, value) in zip(columns, metrics.items()):
            with column:
                st.metric(label, value)

    @staticmethod
    def success(message: str):
        st.success(message)

    @staticmethod
    def warning(message: str):
        st.warning(message)

    @staticmethod
    def error(message: str):
        st.error(message)

    @staticmethod
    def info(message: str):
        st.info(message)

    @staticmethod
    def loading(message="Loading..."):
        """
        Spinner context manager.

        Usage:
        with ui.loading("Loading dataset..."):
            ...
        """
        return st.spinner(message)

    @staticmethod
    def empty_state(message="No data available."):
        st.info(message)

    @staticmethod
    def section(title: str):
        st.subheader(title)

    @staticmethod
    def dataframe(df):
        st.dataframe(
            df,
            use_container_width=True
        )

    @staticmethod
    def footer():

        st.divider()

        st.caption(
            f"{theme.APP_NAME} | Version {theme.APP_VERSION}"
        )


ui = DashboardUI()
