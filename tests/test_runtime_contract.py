"""Runtime and source-data contract tests for the dashboard."""

from pathlib import Path

import pandas as pd
import pytest

from config.config import DATASET_PATH
from src.model_loader import ModelArtifactError, ModelLoader


REQUIRED_DATA_COLUMNS = {
    "incident_id",
    "incident_date",
    "sector",
    "region",
    "attack_type",
    "threat_actor",
    "records_affected",
    "detection_time_hours",
    "ransom_demand_usd",
    "severity_score",
}


def test_source_dataset_matches_contract():
    assert DATASET_PATH == Path("data/raw/cybersecurity_incident_reports.csv")
    assert DATASET_PATH.is_file()
    columns = set(pd.read_csv(DATASET_PATH, nrows=1).columns)
    assert REQUIRED_DATA_COLUMNS.issubset(columns)


def test_model_loader_fails_closed_when_artifacts_are_missing(tmp_path: Path):
    loader = ModelLoader(
        model_path=tmp_path / "best_model.pkl",
        preprocessor_path=tmp_path / "preprocessor.pkl",
        feature_columns_path=tmp_path / "feature_columns.pkl",
    )
    with pytest.raises(ModelArtifactError, match="Trained regression model"):
        loader.load()
