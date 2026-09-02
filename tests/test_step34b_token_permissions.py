from pathlib import Path


WORKFLOW = Path(".github/workflows/sync-part2-artifacts.yml")


def test_artifact_sync_write_permissions_are_job_scoped():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "permissions:\n  contents: write\n  pull-requests: write" not in text
    assert "jobs:\n  sync:\n    permissions:\n      contents: write\n      pull-requests: write" in text


def test_artifact_sync_token_is_used_only_for_pr_creation():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "GH_TOKEN: ${{ github.token }}" in text
    token_block = text.split("GH_TOKEN: ${{ github.token }}", 1)[1]
    assert "gh pr create" in token_block
    assert "git push --set-upstream origin" in token_block


def test_artifact_sync_does_not_request_unrelated_write_scopes():
    text = WORKFLOW.read_text(encoding="utf-8")
    permission_block = text.split("jobs:\n  sync:\n    permissions:\n", 1)[1].split("    runs-on:", 1)[0]
    assert permission_block.strip() == "contents: write\n      pull-requests: write"
