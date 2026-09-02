"""Regression tests for the Streamlit prediction-page error boundary."""

import io

from pages import Prediction


class Upload(io.BytesIO):
    @property
    def size(self):
        return getattr(self, "_size_override", len(self.getbuffer()))


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


def test_prediction_page_rejects_malformed_csv_before_prediction(monkeypatch):
    """Malformed CSV must stop at the parser boundary and never call prediction."""
    upload = Upload(b"a,b\n1,\"unterminated\n")
    errors = []

    monkeypatch.setattr(Prediction.st, "file_uploader", lambda *args, **kwargs: upload)
    monkeypatch.setattr(Prediction.st, "error", errors.append)
    monkeypatch.setattr(Prediction.st, "success", lambda *args, **kwargs: None)

    def fail_if_prediction_called(*args, **kwargs):
        raise AssertionError("Prediction must not run after CSV parser rejection")

    monkeypatch.setattr(Prediction, "predict_incident", fail_if_prediction_called)
    Prediction.render()

    assert errors
    assert "malformed" in errors[-1].lower()
    assert "/" not in errors[-1]
    assert "\\" not in errors[-1]


def test_prediction_page_rejects_oversized_upload_before_parser(monkeypatch):
    """A file over the configured byte boundary must never reach the parser."""
    upload = Upload(b"a,b\n1,2\n")
    upload._size_override = 100 * 1024 * 1024 + 1
    errors = []

    monkeypatch.setattr(Prediction.st, "file_uploader", lambda *args, **kwargs: upload)
    monkeypatch.setattr(Prediction.st, "error", errors.append)
    monkeypatch.setattr(
        Prediction,
        "read_bounded_csv",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("parser must not run")
        ),
    )

    Prediction.render()
    assert errors
    assert "100 MB limit" in errors[-1]
