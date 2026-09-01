"""Load and validate the complete Part 2 runtime artifact contract."""

from pathlib import Path

import joblib

from config.config import FEATURE_COLUMNS_PATH, MODEL_PATH, PREPROCESSOR_PATH


class ModelArtifactError(FileNotFoundError):
    """Raised when a required Part 2 runtime artifact is unavailable."""


class ModelLoader:
    def __init__(
        self,
        model_path=MODEL_PATH,
        preprocessor_path=PREPROCESSOR_PATH,
        feature_columns_path=FEATURE_COLUMNS_PATH,
    ):
        self.model_path = Path(model_path)
        self.preprocessor_path = Path(preprocessor_path)
        self.feature_columns_path = Path(feature_columns_path)
        self.model = None
        self.preprocessor = None
        self.feature_columns = None

    @staticmethod
    def _require(path: Path, label: str):
        if not path.is_file():
            raise ModelArtifactError(
                f"{label} not found at {path}. "
                "Run the Part 2 artifact sync workflow before using predictions."
            )
        if path.stat().st_size == 0:
            raise ModelArtifactError(f"{label} is empty: {path}")

    def load(self):
        self._require(self.model_path, "Trained regression model")
        self._require(self.preprocessor_path, "Preprocessor")
        self._require(self.feature_columns_path, "Feature column contract")
        try:
            model = joblib.load(self.model_path)
            preprocessor = joblib.load(self.preprocessor_path)
            feature_columns = list(joblib.load(self.feature_columns_path))
        except Exception as error:
            raise RuntimeError(f"Unable to load Part 2 artifacts: {error}") from error

        if not hasattr(model, "predict"):
            raise RuntimeError("Loaded model does not expose a predict() method.")
        if not hasattr(preprocessor, "transform"):
            raise RuntimeError("Loaded preprocessor does not expose transform().")
        if not feature_columns or len(set(map(str, feature_columns))) != len(feature_columns):
            raise RuntimeError("Feature column contract must be non-empty and unique.")

        self.model = model
        self.preprocessor = preprocessor
        self.feature_columns = feature_columns
        return self

    def get_artifacts(self):
        if self.model is None:
            self.load()
        return self.model, self.preprocessor, self.feature_columns


def load_runtime_artifacts():
    return ModelLoader().get_artifacts()
