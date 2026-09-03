"""Pre-extraction security validation for the pinned Part 2 runtime bundle."""

from __future__ import annotations

import stat
import zipfile
from pathlib import Path, PurePosixPath

EXPECTED_BUNDLE_MEMBERS = frozenset(
    {
        "artifact_manifest.json",
        "models/best_model.pkl",
        "models/preprocessor.pkl",
        "models/feature_columns.pkl",
        "outputs/evaluation_report.json",
        "outputs/metrics.json",
        "outputs/feature_importance.csv",
    }
)


def validate_runtime_bundle(archive: Path) -> None:
    """Reject unsafe or unexpected ZIP members before any extraction occurs."""
    with zipfile.ZipFile(archive) as zf:
        infos = zf.infolist()
        names = [info.filename for info in infos]

        if len(names) != len(set(names)):
            raise ValueError("Runtime bundle contains duplicate ZIP member names")

        if set(names) != EXPECTED_BUNDLE_MEMBERS:
            raise ValueError(
                "Runtime bundle member contract mismatch: "
                f"expected={sorted(EXPECTED_BUNDLE_MEMBERS)}, actual={sorted(names)}"
            )

        for info in infos:
            name = info.filename
            path = PurePosixPath(name)
            if not name or path.is_absolute() or ".." in path.parts:
                raise ValueError(f"Unsafe ZIP member path: {name!r}")
            if "\\" in name:
                raise ValueError(f"Unsafe ZIP member path separator: {name!r}")
            if info.is_dir():
                raise ValueError(f"Directory ZIP members are not allowed: {name!r}")

            mode = (info.external_attr >> 16) & 0o177777
            if stat.S_ISLNK(mode):
                raise ValueError(f"Symlink ZIP members are not allowed: {name!r}")


def safe_extract_runtime_bundle(archive: Path, destination: Path) -> None:
    """Validate then extract the trusted, exact runtime bundle."""
    validate_runtime_bundle(archive)
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(destination)
