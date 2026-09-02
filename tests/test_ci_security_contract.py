from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / ".github" / "workflows" / "ci.yml"
SYNC = ROOT / ".github" / "workflows" / "sync-part2-artifacts.yml"
EXPECTED_BUNDLE_SHA256 = "ece2b6bf91f19e5c0eb19475ae7198155f3fdaa4e8839ec9ab95f8cfcf031d54"
CHECKOUT_SHA = "d23441a48e516b6c34aea4fa41551a30e30af803"
SETUP_PYTHON_SHA = "ece7cb06caefa5fff74198d8649806c4678c61a1"


def test_ci_pins_external_action_commits():
    text = CI.read_text(encoding="utf-8")
    assert f"actions/checkout@{CHECKOUT_SHA}" in text
    assert f"actions/setup-python@{SETUP_PYTHON_SHA}" in text
    assert "actions/checkout@v6" not in text
    assert "actions/setup-python@v6" not in text


def test_ci_pins_part2_bundle_digest():
    text = CI.read_text(encoding="utf-8")
    assert f'PART2_BUNDLE_SHA256: "{EXPECTED_BUNDLE_SHA256}"' in text
    assert "sha256sum .part2-runtime/artifacts.zip" in text
    assert "$actual_sha256 != \"$PART2_BUNDLE_SHA256\"" not in text
    assert "$actual_sha256" in text


def test_sync_workflow_has_no_user_selectable_release_tag():
    text = SYNC.read_text(encoding="utf-8")
    assert "inputs:" not in text
    assert "inputs.part2_release_tag" not in text
    assert 'PART2_RELEASE_TAG: "part2-runtime-33513838252"' in text
    assert f'PART2_BUNDLE_SHA256: "{EXPECTED_BUNDLE_SHA256}"' in text
    assert "sha256sum .part2-runtime/artifacts.zip" in text


def test_sync_workflow_pins_external_action_commits():
    text = SYNC.read_text(encoding="utf-8")
    assert f"actions/checkout@{CHECKOUT_SHA}" in text
    assert f"actions/setup-python@{SETUP_PYTHON_SHA}" in text
    assert "actions/checkout@v6" not in text
    assert "actions/setup-python@v6" not in text
