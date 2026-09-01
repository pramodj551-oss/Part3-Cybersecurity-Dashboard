"""Visualization helpers for the Streamlit dashboard."""

import pandas as pd
import plotly.express as px
import streamlit as st


class DashboardVisualizer:
    """Visualization utilities for dashboard pages."""

    @staticmethod
    def display_dataset_overview(df: pd.DataFrame):
        st.subheader("Dataset Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", len(df))
        col2.metric("Columns", len(df.columns))
        col3.metric("Missing Values", int(df.isnull().sum().sum()))

    @staticmethod
    def display_dataframe(df: pd.DataFrame):
        st.subheader("Dataset Preview")
        st.dataframe(df, use_container_width=True)

    @staticmethod
    def plot_missing_values(df: pd.DataFrame):
        missing = df.isnull().sum().sort_values(ascending=False)
        missing = missing[missing > 0]
        if missing.empty:
            st.success("No missing values found.")
            return
        fig = px.bar(
            x=missing.index,
            y=missing.values,
            labels={"x": "Features", "y": "Missing Values"},
            title="Missing Value Analysis",
        )
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_target_distribution(df: pd.DataFrame, target_column: str):
        if target_column not in df.columns:
            st.warning("Target column not found.")
            return
        fig = px.histogram(df, x=target_column, title="Target Variable Distribution")
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_correlation(df: pd.DataFrame):
        numeric = df.select_dtypes(include="number")
        if numeric.shape[1] < 2:
            st.warning("At least two numerical columns are required for correlation analysis.")
            return
        correlation = numeric.corr()
        fig = px.imshow(
            correlation,
            text_auto=True,
            aspect="auto",
            title="Correlation Heatmap",
        )
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_feature_importance(importance_df: pd.DataFrame):
        """Plot either the normalized STEP 20 or legacy title-cased contract."""
        column_map = {str(column).lower(): column for column in importance_df.columns}
        feature_column = column_map.get("feature")
        importance_column = column_map.get("importance")
        if feature_column is None or importance_column is None:
            raise ValueError("Feature-importance data must contain Feature and Importance columns.")

        display = importance_df[[feature_column, importance_column]].copy()
        display.columns = ["Feature", "Importance"]
        display["Importance"] = pd.to_numeric(display["Importance"], errors="coerce")
        display = display.dropna(subset=["Importance"])
        if display.empty:
            st.warning("No valid feature-importance values are available.")
            return

        fig = px.bar(
            display,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Feature Importance",
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)


visualizer = DashboardVisualizer()
