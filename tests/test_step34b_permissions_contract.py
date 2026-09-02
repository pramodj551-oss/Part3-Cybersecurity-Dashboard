from pathlib import Path


WORKFLOW = Path('.github/workflows/sync-part2-artifacts.yml')


def test_sync_workflow_scopes_write_permissions_to_sync_job():
    text = WORKFLOW.read_text(encoding='utf-8')
    assert 'permissions:\n  contents: write\n  pull-requests: write' not in text
    assert '  sync:\n    permissions:\n      contents: write\n      pull-requests: write\n' in text


def test_sync_workflow_retains_required_token_operations():
    text = WORKFLOW.read_text(encoding='utf-8')
    assert 'GH_TOKEN: ${{ github.token }}' in text
    assert 'git push --set-upstream origin "$sync_branch"' in text
    assert 'gh pr create \' in text


def test_sync_workflow_requests_only_required_write_scopes():
    text = WORKFLOW.read_text(encoding='utf-8')
    block = text.split('  sync:\n    permissions:\n', 1)[1].split('    runs-on:', 1)[0]
    assert block == '      contents: write\n      pull-requests: write\n'
