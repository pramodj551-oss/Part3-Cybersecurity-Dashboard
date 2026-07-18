"""
==========================================================
AI-Powered Cybersecurity Dashboard
Theme Module
Version: 3.0
==========================================================

Centralized theme configuration for the Streamlit dashboard.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardTheme:
    """
    Dashboard theme configuration.
    """

    # ------------------------------------------------------
    # Branding
    # ------------------------------------------------------

    APP_NAME = "AI-Powered Cybersecurity Dashboard"

    APP_VERSION = "3.0"

    APP_ICON = "🛡️"

    # ------------------------------------------------------
    # Primary Colors
    # ------------------------------------------------------

    PRIMARY = "#1565C0"

    SECONDARY = "#42A5F5"

    SUCCESS = "#2E7D32"

    WARNING = "#ED6C02"

    ERROR = "#D32F2F"

    INFO = "#0288D1"

    # ------------------------------------------------------
    # Background
    # ------------------------------------------------------

    BACKGROUND = "#F8F9FA"

    CARD = "#FFFFFF"

    SIDEBAR = "#F5F7FA"

    # ------------------------------------------------------
    # Text
    # ------------------------------------------------------

    TEXT_PRIMARY = "#212121"

    TEXT_SECONDARY = "#616161"

    # ------------------------------------------------------
    # Charts
    # ------------------------------------------------------

    CHART_COLORS = [

        "#1565C0",
        "#42A5F5",
        "#66BB6A",
        "#FFA726",
        "#EF5350",
        "#AB47BC",
        "#26A69A"

    ]

    # ------------------------------------------------------
    # Icons
    # ------------------------------------------------------

    HOME = "🏠"

    DATASET = "📊"

    EDA = "📈"

    PREDICTION = "🤖"

    FEATURE = "⭐"

    PERFORMANCE = "📉"

    SETTINGS = "⚙️"


theme = DashboardTheme()
