"""Model loading utilities with clear artifact diagnostics."""

from pathlib import Path
from typing import Optional

import joblib

from config.config import MODEL_PATH


class ModelArtifactError(FileNotFoundError):
    """Raised when the trained model artifact is unavailable."""


class ModelLoader:
    def __init__(self, model_path=MODEL_PATH):
        self.model_path = Path(model_path)
        self.model = None

    def model_exists(self) -> bool:
        return self.model_path.is_file()

    def artifact_message(self) -> str:
        return (
            f"Trained model not found at: {self.model_path}. "
            "Run the Part 2 training pipeline and copy the exact model artifact "
            "to this repository, or configure MODEL_PATH."
        )

    def load_model(self):
        if not self.model_exists():
            raise ModelArtifactError(self.artifact_message())

        try:
            self.model = joblib.load(self.model_path)
        except Exception as error:
            raise RuntimeError(
                f"Unable to load model artifact '{self.model_path}': {error}"
            ) from error
        return self.model

    def get_model(self):
        if self.model is None:
            self.load_model()
        return self.model


def load_trained_model():
    return ModelLoader().get_model()
