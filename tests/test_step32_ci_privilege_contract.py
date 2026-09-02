from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / ".github" / "workflows" / "ci.yml"
SYNC = ROOT / ".github" / "workflows" / "sync-part2-artifacts.yml"


def test_normal_ci_is_read_only():
    text = CI.read_text(encoding="utf-8")
    assert "permissions:\n  contents: read" in text
    assert "contents: write" not in text
    assert "pull-requests: write" not in text


def test_sync_is_manual_and_pr_based():
    text = SYNC.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in text
    assert "pull-requests: write" in text
    assert "contents: write" in text
    assert 'git push --set-upstream origin "$sync_branch"' in text
    assert 'gh pr create' in text
    assert 'git push\n' not in text


def test_sync_never_pushes_directly_to_main():
    text = SYNC.read_text(encoding="utf-8")
    assert 'git checkout -b "$sync_branch"' in text
    assert 'sync_branch="automation/part2-runtime-sync-${GITHUB_RUN_ID}"' in text
    assert "--base main" in text
    assert "--head \"$sync_branch\"" in text


def test_sync_has_no_user_selectable_release_or_branch_input():
    text = SYNC.read_text(encoding="utf-8")
    assert "inputs:" not in text
    assert "inputs.part2_release_tag" not in text
    assert "inputs.sync_branch" not in text


def test_privileged_workflow_has_no_pull_request_trigger():
    text = SYNC.read_text(encoding="utf-8")
    assert "pull_request:" not in text
    assert "pull_request_target:" not in text
