"""
==========================================================
AI-Powered Cybersecurity Dashboard
Model Loader Module
Version: 3.0
==========================================================
"""

from pathlib import Path
import joblib

from config.config import MODEL_PATH


class ModelLoader:
    """
    Utility class for loading trained machine learning models.
    """

    def __init__(self, model_path=MODEL_PATH):
        self.model_path = Path(model_path)
        self.model = None

    def model_exists(self) -> bool:
        """
        Check whether the trained model exists.
        """
        return self.model_path.exists()

    def load_model(self):
        """
        Load the trained model from disk.
        """
        if not self.model_exists():
            raise FileNotFoundError(
                f"Model not found: {self.model_path}"
            )

        self.model = joblib.load(self.model_path)

        return self.model

    def get_model(self):
        """
        Return the loaded model.
        """
        if self.model is None:
            self.load_model()

        return self.model


def load_trained_model():
    """
    Convenience function for loading the trained model.
    """
    loader = ModelLoader()
    return loader.get_model()


if __name__ == "__main__":

    try:

        model = load_trained_model()

        print("=" * 60)
        print("MODEL LOADED SUCCESSFULLY")
        print("=" * 60)

        print(type(model))

    except Exception as error:

        print("=" * 60)
        print("MODEL LOADING FAILED")
        print("=" * 60)

        print(error)
