"""
==========================================================
AI-Powered Cybersecurity Dashboard
Configuration Module
Version: 3.0
==========================================================
"""

from pathlib import Path


# ==========================================================
# Project Directories
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"
ASSETS_DIR = PROJECT_ROOT / "assets"

IMAGES_DIR = ASSETS_DIR / "images"
STYLES_DIR = ASSETS_DIR / "styles"

# ==========================================================
# Dataset Configuration
# ==========================================================

DATASET_NAME = "cybersecurity_incidents.csv"
DATASET_PATH = DATA_DIR / DATASET_NAME

# ==========================================================
# Model Configuration
# ==========================================================

MODEL_NAME = "random_forest_model.pkl"
MODEL_PATH = MODELS_DIR / MODEL_NAME

# ==========================================================
# Output Files
# ==========================================================

PREDICTION_OUTPUT = OUTPUTS_DIR / "prediction_results.csv"
FEATURE_IMPORTANCE_OUTPUT = OUTPUTS_DIR / "feature_importance.csv"
EVALUATION_REPORT = OUTPUTS_DIR / "evaluation_report.csv"

# ==========================================================
# Logging
# ==========================================================

LOG_FILE = LOGS_DIR / "dashboard.log"
LOG_LEVEL = "INFO"

# ==========================================================
# Streamlit Configuration
# ==========================================================

APP_TITLE = "AI-Powered Cybersecurity Dashboard"

APP_ICON = "🛡️"

LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

# ==========================================================
# Machine Learning
# ==========================================================

TARGET_COLUMN = "severity"

RANDOM_STATE = 42

TEST_SIZE = 0.20

# ==========================================================
# Visualization
# ==========================================================

FIGURE_WIDTH = 10

FIGURE_HEIGHT = 6

MAX_PLOT_COLUMNS = 12

# ==========================================================
# Dashboard Settings
# ==========================================================

MAX_UPLOAD_SIZE_MB = 100

SUPPORTED_FILE_TYPES = [
    "csv"
]

DEFAULT_SAMPLE_SIZE = 100

# ==========================================================
# Create Required Directories
# ==========================================================

for directory in [
    DATA_DIR,
    MODELS_DIR,
    OUTPUTS_DIR,
    LOGS_DIR,
    ASSETS_DIR,
    IMAGES_DIR,
    STYLES_DIR,
]:
    directory.mkdir(
        parents=True,
        exist_ok=True
    )

# ==========================================================
# End of Configuration
# ==========================================================
