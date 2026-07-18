"""
==========================================================
AI-Powered Cybersecurity Dashboard
Visualization Module
Version: 3.0
==========================================================
"""

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st


class DashboardVisualizer:
    """
    Visualization utilities for the Streamlit dashboard.
    """

    @staticmethod
    def display_dataset_overview(df: pd.DataFrame):

        st.subheader("Dataset Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", len(df))
        col2.metric("Columns", len(df.columns))
        col3.metric(
            "Missing Values",
            int(df.isnull().sum().sum())
        )

    @staticmethod
    def display_dataframe(df: pd.DataFrame):

        st.subheader("Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

    @staticmethod
    def plot_missing_values(df: pd.DataFrame):

        missing = (
            df.isnull()
              .sum()
              .sort_values(ascending=False)
        )

        missing = missing[missing > 0]

        if missing.empty:

            st.success("No missing values found.")

            return

        fig = px.bar(
            x=missing.index,
            y=missing.values,
            labels={
                "x": "Features",
                "y": "Missing Values"
            },
            title="Missing Value Analysis"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    @staticmethod
    def plot_target_distribution(
        df: pd.DataFrame,
        target_column: str
    ):

        if target_column not in df.columns:

            st.warning("Target column not found.")

            return

        fig = px.histogram(
            df,
            x=target_column,
            title="Target Variable Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    @staticmethod
    def plot_correlation(df: pd.DataFrame):

        numeric = df.select_dtypes(
            include="number"
        )

        if numeric.empty:

            st.warning(
                "No numerical columns available."
            )

            return

        correlation = numeric.corr()

        fig = px.imshow(
            correlation,
            text_auto=True,
            aspect="auto",
            title="Correlation Heatmap"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    @staticmethod
    def plot_feature_importance(
        importance_df: pd.DataFrame
    ):

        fig = px.bar(
            importance_df,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Feature Importance"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ----------------------------------------------------------
# Convenience Object
# ----------------------------------------------------------

visualizer = DashboardVisualizer()
