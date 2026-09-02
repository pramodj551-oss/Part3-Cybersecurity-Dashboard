"""Load and validate the complete Part 2 runtime artifact contract."""

from pathlib import Path
import pickle

import joblib

from config.config import FEATURE_COLUMNS_PATH, MODEL_PATH, PREPROCESSOR_PATH
from src.runtime_artifact_identity import verify_runtime_artifact_identity


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

    @staticmethod
    def _load_feature_columns(path: Path):
        """Load feature_columns.pkl from Part 2's pickle/joblib formats.

        Part 2 may serialize this simple Python sequence with either
        ``pickle.dump`` or ``joblib.dump``.  Prefer the standard pickle
        protocol first, then fall back to joblib for compatibility.
        """
        pickle_error = None
        try:
            with path.open("rb") as handle:
                return list(pickle.load(handle))
        except Exception as error:
            pickle_error = error

        try:
            return list(joblib.load(path))
        except Exception as joblib_error:
            raise RuntimeError(
                "Unable to deserialize feature column contract "
                f"{path} using pickle or joblib. "
                f"pickle_error={pickle_error}; joblib_error={joblib_error}"
            ) from joblib_error

    def load(self):
        self._require(self.model_path, "Trained regression model")
        self._require(self.preprocessor_path, "Preprocessor")
        self._require(self.feature_columns_path, "Feature column contract")

        production_paths = (
            self.model_path == Path(MODEL_PATH)
            and self.preprocessor_path == Path(PREPROCESSOR_PATH)
            and self.feature_columns_path == Path(FEATURE_COLUMNS_PATH)
        )
        if not production_paths:
            raise ModelArtifactError(
                "ModelLoader refuses to deserialize artifacts outside the configured production paths."
            )

        ok, _, message = verify_runtime_artifact_identity()
        if not ok:
            raise ModelArtifactError(
                "Runtime artifact identity verification failed; refusing to deserialize artifacts. "
                f"{message}"
            )

        try:
            model = joblib.load(self.model_path)
            preprocessor = joblib.load(self.preprocessor_path)
            feature_columns = self._load_feature_columns(self.feature_columns_path)
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
    """Load production artifacts through the identity-gated ModelLoader."""
    loader = ModelLoader().load()
    return loader.model, loader.preprocessor, loader.feature_columns
