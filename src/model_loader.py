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

    def _require(self, path: Path, label: str):
        if not path.is_file():
            raise ModelArtifactError(
                f"{label} not found at {path}. "
                "Run the Part 2 artifact sync workflow before using predictions."
            )

    def load(self):
        self._require(self.model_path, "Trained regression model")
        self._require(self.preprocessor_path, "Preprocessor")
        self._require(self.feature_columns_path, "Feature column contract")
        try:
            self.model = joblib.load(self.model_path)
            self.preprocessor = joblib.load(self.preprocessor_path)
            self.feature_columns = list(joblib.load(self.feature_columns_path))
        except Exception as error:
            raise RuntimeError(f"Unable to load Part 2 artifacts: {error}") from error
        return self

    def get_artifacts(self):
        if self.model is None:
            self.load()
        return self.model, self.preprocessor, self.feature_columns


def load_runtime_artifacts():
    return ModelLoader().get_artifacts()
