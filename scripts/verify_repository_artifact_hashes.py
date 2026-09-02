from __future__ import annotations

import hashlib
import json
from pathlib import Path

MANIFEST = Path("models/artifact_manifest.json")


def main() -> None:
    if not MANIFEST.is_file():
        raise SystemExit(f"Missing artifact manifest: {MANIFEST}")

    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = payload.get("files")
    required = {
        "models/best_model.pkl",
        "models/preprocessor.pkl",
        "models/feature_columns.pkl",
        "outputs/evaluation_report.json",
        "outputs/metrics.json",
        "outputs/feature_importance.csv",
    }
    if set(expected or {}) != required:
        raise SystemExit(
            f"Artifact manifest contract mismatch: {sorted(expected or {})}"
        )

    failures: list[str] = []
    matches = 0
    for relative in sorted(required):
        path = Path(relative)
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"{relative}: missing or empty")
            print(f"FAIL artifact: {relative} — missing or empty")
            continue

        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        expected_hash = expected[relative]
        if actual == expected_hash:
            matches += 1
            print(f"PASS SHA256: {relative} = {actual}")
        else:
            failures.append(f"{relative}: {actual} != {expected_hash}")
            print(f"FAIL SHA256: {relative}")
            print(f"  actual:   {actual}")
            print(f"  expected: {expected_hash}")

    print(f"SHA256 identity result: {matches}/6 exact matches")
    if failures:
        raise SystemExit("Repository artifact cryptographic identity check FAILED")
    print("PASS 6/6 repository artifacts match artifact_manifest.json SHA256 values")


if __name__ == "__main__":
    main()
