from pathlib import Path
from zipfile import ZipFile, ZipInfo

import pytest

from scripts.validate_runtime_bundle import EXPECTED_MEMBERS, validate_zip_members


def _write_zip(path: Path, names, symlink_name=None):
    with ZipFile(path, "w") as zf:
        for name in names:
            info = ZipInfo(name)
            if name == symlink_name:
                info.external_attr = (0o120777 << 16)
            zf.writestr(info, b"x")


def test_safe_runtime_bundle_is_accepted(tmp_path):
    archive = tmp_path / "safe.zip"
    _write_zip(archive, sorted(EXPECTED_MEMBERS))
    validate_zip_members(archive)


@pytest.mark.parametrize("bad_name", ["../escape.txt", "/absolute.txt", "models/../escape.txt"])
def test_path_traversal_or_absolute_member_is_rejected(tmp_path, bad_name):
    archive = tmp_path / "unsafe.zip"
    names = sorted(EXPECTED_MEMBERS - {"artifact_manifest.json"}) + [bad_name, "artifact_manifest.json"]
    _write_zip(archive, names)
    with pytest.raises(ValueError):
        validate_zip_members(archive)


def test_symlink_member_is_rejected(tmp_path):
    archive = tmp_path / "symlink.zip"
    _write_zip(archive, sorted(EXPECTED_MEMBERS), symlink_name="models/best_model.pkl")
    with pytest.raises(ValueError, match="Symlink"):
        validate_zip_members(archive)


def test_duplicate_member_is_rejected(tmp_path):
    archive = tmp_path / "duplicate.zip"
    names = sorted(EXPECTED_MEMBERS)
    with ZipFile(archive, "w") as zf:
        for name in names:
            zf.writestr(name, b"x")
        zf.writestr(names[0], b"duplicate")
    with pytest.raises(ValueError, match="Duplicate"):
        validate_zip_members(archive)


def test_unexpected_member_is_rejected(tmp_path):
    archive = tmp_path / "extra.zip"
    _write_zip(archive, sorted(EXPECTED_MEMBERS | {"unexpected.txt"}))
    with pytest.raises(ValueError, match="contract mismatch"):
        validate_zip_members(archive)
