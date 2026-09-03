"""Security validation for downloaded Part 2 runtime ZIP bundles."""
from __future__ import annotations

import posixpath
import stat
from pathlib import Path
from zipfile import BadZipFile, ZipFile

EXPECTED_FILES = {
    "artifact_manifest.json",
    "models/best_model.pkl",
    "models/preprocessor.pkl",
    "models/feature_columns.pkl",
    "outputs/evaluation_report.json",
    "outputs/metrics.json",
    "outputs/feature_importance.csv",
}
EXPECTED_DIRECTORIES = {"models/", "outputs/"}
EXPECTED_MEMBERS = EXPECTED_FILES | EXPECTED_DIRECTORIES


def validate_zip_members(archive: Path) -> None:
    """Fail closed before extraction on unsafe or unexpected ZIP members."""
    try:
        with ZipFile(archive) as zf:
            infos = zf.infolist()
    except (BadZipFile, OSError) as exc:
        raise ValueError(f"Invalid runtime bundle: {exc}") from exc

    names = [info.filename for info in infos]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate ZIP member names are not allowed")

    if set(names) != EXPECTED_MEMBERS:
        raise ValueError(
            f"Runtime bundle member contract mismatch: {sorted(names)}"
        )

    for info in infos:
        name = info.filename
        if not name or "\\" in name:
            raise ValueError(f"Unsafe ZIP member path: {name!r}")
        normalized = posixpath.normpath(name)
        if normalized != name and name not in EXPECTED_DIRECTORIES:
            raise ValueError(f"Path traversal ZIP member: {name!r}")
        if normalized.startswith("../") or normalized == "..":
            raise ValueError(f"Path traversal ZIP member: {name!r}")
        if name.startswith("/") or Path(name).is_absolute():
            raise ValueError(f"Absolute ZIP member path: {name!r}")
        mode = (info.external_attr >> 16) & 0o170000
        if mode == stat.S_IFLNK:
            raise ValueError(f"Symlink ZIP member is not allowed: {name!r}")
        if name in EXPECTED_DIRECTORIES:
            if not info.is_dir():
                raise ValueError(f"Expected ZIP directory is not a directory: {name!r}")
            continue
        if info.is_dir():
            raise ValueError(f"Unexpected directory ZIP member: {name!r}")
        if info.file_size == 0:
            raise ValueError(f"Empty ZIP member is not allowed: {name!r}")
