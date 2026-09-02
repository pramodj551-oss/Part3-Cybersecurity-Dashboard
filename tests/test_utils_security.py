from pathlib import Path

import pytest

import src.utils as utils


def test_load_dataset_rejects_path_outside_data_root(tmp_path, monkeypatch):
    data_root = tmp_path / "data"
    data_root.mkdir()
    outside = tmp_path / "outside.csv"
    outside.write_text("a,b\n1,2\n", encoding="utf-8")
    monkeypatch.setattr(utils, "DATA_DIR", data_root)

    with pytest.raises(ValueError, match="inside the configured data directory"):
        utils.load_dataset(outside)


def test_load_dataset_rejects_symlink_escape(tmp_path, monkeypatch):
    data_root = tmp_path / "data"
    data_root.mkdir()
    outside = tmp_path / "outside.csv"
    outside.write_text("a,b\n1,2\n", encoding="utf-8")
    link = data_root / "linked.csv"
    link.symlink_to(outside)
    monkeypatch.setattr(utils, "DATA_DIR", data_root)

    with pytest.raises(ValueError, match="inside the configured data directory"):
        utils.load_dataset(link)


def test_load_dataset_allows_file_inside_data_root(tmp_path, monkeypatch):
    data_root = tmp_path / "data"
    data_root.mkdir()
    dataset = data_root / "dataset.csv"
    dataset.write_text("a,b\n1,2\n", encoding="utf-8")
    monkeypatch.setattr(utils, "DATA_DIR", data_root)

    result = utils.load_dataset(dataset)

    assert list(result.columns) == ["a", "b"]
    assert len(result) == 1


def test_load_dataset_rejects_parent_traversal(tmp_path, monkeypatch):
    data_root = tmp_path / "data"
    data_root.mkdir()
    outside = tmp_path / "outside.csv"
    outside.write_text("a,b\n1,2\n", encoding="utf-8")
    monkeypatch.setattr(utils, "DATA_DIR", data_root)

    traversal = Path(data_root) / ".." / "outside.csv"
    with pytest.raises(ValueError, match="inside the configured data directory"):
        utils.load_dataset(traversal)
