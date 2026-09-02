"""Read-only runtime deployment fingerprint helpers."""

from __future__ import annotations

import os
import subprocess


def get_runtime_commit() -> str:
    """Return the commit checked out by the runtime, never a hard-coded SHA."""
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
        if commit:
            return commit
    except (OSError, subprocess.SubprocessError):
        pass

    for key in ("GIT_COMMIT", "COMMIT_SHA", "STREAMLIT_GIT_COMMIT"):
        value = os.getenv(key, "").strip()
        if value:
            return value

    return "unavailable"
