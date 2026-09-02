"""End-to-end smoke test using the synchronized Part 2 runtime artifacts."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd

from config.config import DATASET_PATH, PREDICTION_FEATURES, TARGET_COLUMN
from src.prediction import PredictionEngine
from src.runtime_artifact_identity import verify_runtime_artifact_identity


REQUIRED_ARTIFACTS = [
    ROOT / "models/best_model.pkl",
    ROOT / "models/preprocessor.pkl",
    ROOT / "models/feature_columns.pkl",
    ROOT / "outputs/evaluation_report.json",
    ROOT / "outputs/metrics.json",
    ROOT / "outputs/feature_importance.csv",
]
GOLDEN_FIRST_PREDICTION = 4.669436934238102
GOLDEN_TOLERANCE = 1e-12


def main() -> None:
    missing = [str(path) for path in REQUIRED_ARTIFACTS if not path.is_file() or path.stat().st_size == 0]
    if missing:
        raise SystemExit(f"Missing runtime artifacts: {missing}")

    identity_ok, _, identity_message = verify_runtime_artifact_identity()
    if not identity_ok:
        raise SystemExit(f"Runtime artifact identity verification failed: {identity_message}")
    print(f"PASS runtime artifact identity: {identity_message}")

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
    if not pd.api.types.is_numeric_dtype(predictions):
        raise SystemExit("Prediction output is not numeric.")
    if abs(float(predictions[0]) - GOLDEN_FIRST_PREDICTION) > GOLDEN_TOLERANCE:
        raise SystemExit(
            "Prediction golden reference mismatch: "
            f"{predictions[0]!r} != {GOLDEN_FIRST_PREDICTION!r}"
        )

    summary = engine.predict_with_summary(sample)
    expected_columns = list(sample.columns) + ["Predicted_Severity_Score"]
    if list(summary.columns) != expected_columns:
        raise SystemExit("Prediction output schema/order does not match the production contract.")

    print(f"PASS real prediction smoke test: {len(predictions)} prediction(s) generated.")
    print(f"PASS target contract: {TARGET_COLUMN} -> Predicted_Severity_Score")
    print(f"PASS prediction golden reference: {predictions[0]!r}")
    print(f"PASS prediction output schema: {list(summary.columns)!r}")


if __name__ == "__main__":
    main()
