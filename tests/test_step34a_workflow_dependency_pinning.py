from pathlib import Path
import re


WORKFLOW_DIR = Path(__file__).resolve().parents[1] / ".github" / "workflows"
PINNED_PIP_RE = re.compile(
    r'python\s+-m\s+pip\s+install\s+(?:[^\n]*\s+)?["\']pip==\d+\.\d+\.\d+["\']'
)


def test_sync_workflow_pins_pip_bootstrap():
    workflow = (WORKFLOW_DIR / "sync-part2-artifacts.yml").read_text(encoding="utf-8")
    assert "python -m pip install --upgrade pip" not in workflow
    assert PINNED_PIP_RE.search(workflow)


def test_ci_workflow_pins_pip_bootstrap():
    workflow = (WORKFLOW_DIR / "ci.yml").read_text(encoding="utf-8")
    assert "python -m pip install --upgrade pip" not in workflow
    assert PINNED_PIP_RE.search(workflow)
