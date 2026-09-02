"""Regression tests for the Streamlit prediction-page error boundary."""

import io

from pages import Prediction


class Upload(io.BytesIO):
    @property
    def size(self):
        return len(self.getbuffer())


def test_prediction_page_surfaces_missing_feature_error(monkeypatch):
    """UI must expose the actionable production validation error."""
    payload = b"sector,region,attack_type,threat_actor\nEnergy,Asia,Phishing,Unknown\n"
    upload = Upload(payload)
    errors = []

    monkeypatch.setattr(Prediction.st, "file_uploader", lambda *args, **kwargs: upload)
    monkeypatch.setattr(Prediction.st, "button", lambda *args, **kwargs: True)
    monkeypatch.setattr(Prediction.st, "error", errors.append)
    monkeypatch.setattr(Prediction.st, "success", lambda *args, **kwargs: None)
    monkeypatch.setattr(Prediction.st, "info", lambda *args, **kwargs: None)
    monkeypatch.setattr(Prediction.st, "subheader", lambda *args, **kwargs: None)
    monkeypatch.setattr(Prediction.st, "dataframe", lambda *args, **kwargs: None)
    monkeypatch.setattr(Prediction.st, "write", lambda *args, **kwargs: None)
    monkeypatch.setattr(Prediction.st, "divider", lambda *args, **kwargs: None)
    monkeypatch.setattr(Prediction.st, "spinner", lambda *args, **kwargs: __import__("contextlib").nullcontext())

    def fail_if_prediction_called(*args, **kwargs):
        raise AssertionError("Prediction must not run when required features are missing")

    monkeypatch.setattr(Prediction, "predict_incident", fail_if_prediction_called)

    Prediction.render()

    assert errors
    assert "Prediction input is missing required features" in errors[-1]
    assert "records_affected" in errors[-1]
    assert "Prediction failed. Please verify" not in errors[-1]
