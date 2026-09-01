"""End-to-end smoke test using the synchronized Part 2 runtime artifacts."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd

from config.config import DATASET_PATH, PREDICTION_FEATURES, TARGET_COLUMN
from src.prediction import PredictionEngine


REQUIRED_ARTIFACTS = [
    ROOT / "models/best_model.pkl",
    ROOT / "models/preprocessor.pkl",
    ROOT / "models/feature_columns.pkl",
    ROOT / "outputs/evaluation_report.json",
    ROOT / "outputs/metrics.json",
    ROOT / "outputs/feature_importance.csv",
]


def main() -> None:
    missing = [str(path) for path in REQUIRED_ARTIFACTS if not path.is_file() or path.stat().st_size == 0]
    if missing:
        raise SystemExit(f"Missing runtime artifacts: {missing}")

    source = pd.read_csv(DATASET_PATH, nrows=1)
    missing_features = [column for column in PREDICTION_FEATURES if column not in source.columns]
    if missing_features:
        raise SystemExit(f"Smoke-test dataset is missing prediction features: {missing_features}")

    sample = source.loc[:, PREDICTION_FEATURES].copy()
    engine = PredictionEngine()
    predictions = engine.predict(sample)

    if len(predictions) != len(sample):
        raise SystemExit("Prediction row count does not match input row count.")
    if pd.isna(predictions).any():
        raise SystemExit("Prediction output contains NaN values.")

    print(f"PASS real prediction smoke test: {len(predictions)} prediction(s) generated.")
    print(f"PASS target contract: {TARGET_COLUMN} -> Predicted_Severity_Score")
    print(f"PASS prediction output: {predictions[0]!r}")


if __name__ == "__main__":
    main()
