"""Regression tests for side-effect-free configuration imports."""

import importlib
from pathlib import Path


def test_config_import_does_not_create_directories(monkeypatch):
    """Importing config must not perform filesystem writes."""

    import config.config as config

    def fail_mkdir(*args, **kwargs):
        raise AssertionError("config import must not call Path.mkdir()")

    monkeypatch.setattr(Path, "mkdir", fail_mkdir)
    importlib.reload(config)


def test_ensure_directories_creates_configured_directories(tmp_path, monkeypatch):
    """Directory creation remains available behind an explicit initializer."""

    import config.config as config

    paths = {
        "DATA_DIR": tmp_path / "data",
        "RAW_DATA_DIR": tmp_path / "data" / "raw",
        "MODELS_DIR": tmp_path / "models",
        "OUTPUTS_DIR": tmp_path / "outputs",
        "LOGS_DIR": tmp_path / "logs",
        "ASSETS_DIR": tmp_path / "assets",
        "IMAGES_DIR": tmp_path / "assets" / "images",
        "STYLES_DIR": tmp_path / "assets" / "styles",
    }
    for name, path in paths.items():
        monkeypatch.setattr(config, name, path)

    config.ensure_directories()

    for path in paths.values():
        assert path.is_dir()
