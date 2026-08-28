"""Configuration for the Part 3 cybersecurity regression dashboard."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"
ASSETS_DIR = PROJECT_ROOT / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
STYLES_DIR = ASSETS_DIR / "styles"

DATASET_NAME = "cybersecurity_incidents.csv"
DATASET_PATH = DATA_DIR / DATASET_NAME

MODEL_NAME = "best_model.pkl"
MODEL_PATH = MODELS_DIR / MODEL_NAME
PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.pkl"
FEATURE_COLUMNS_PATH = MODELS_DIR / "feature_columns.pkl"
MODEL_METADATA_PATH = MODELS_DIR / "model_metadata.json"

PREDICTION_OUTPUT = OUTPUTS_DIR / "prediction_results.csv"
FEATURE_IMPORTANCE_OUTPUT = OUTPUTS_DIR / "feature_importance.csv"
EVALUATION_REPORT = OUTPUTS_DIR / "evaluation_report.json"
METRICS_OUTPUT = OUTPUTS_DIR / "metrics.json"
MODEL_COMPARISON_OUTPUT = OUTPUTS_DIR / "model_comparison.csv"

LOG_FILE = LOGS_DIR / "dashboard.log"
LOG_LEVEL = "INFO"
APP_TITLE = "AI-Powered Cybersecurity Regression Dashboard"
APP_ICON = "🛡️"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"
TARGET_COLUMN = "severity_score"
RANDOM_STATE = 42
TEST_SIZE = 0.20
FIGURE_WIDTH = 10
FIGURE_HEIGHT = 6
MAX_PLOT_COLUMNS = 12
MAX_UPLOAD_SIZE_MB = 100
SUPPORTED_FILE_TYPES = ["csv"]
DEFAULT_SAMPLE_SIZE = 100

for directory in [
    DATA_DIR, MODELS_DIR, OUTPUTS_DIR, LOGS_DIR, ASSETS_DIR,
    IMAGES_DIR, STYLES_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)
