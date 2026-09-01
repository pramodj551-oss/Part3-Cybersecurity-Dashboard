from types import SimpleNamespace

import pytest

from src.upload_validation import validate_upload_size


def test_upload_at_limit_is_allowed():
    upload = SimpleNamespace(size=100 * 1024 * 1024)
    validate_upload_size(upload, 100)


def test_upload_over_limit_is_rejected():
    upload = SimpleNamespace(size=100 * 1024 * 1024 + 1)
    with pytest.raises(ValueError, match="exceeds the 100 MB limit"):
        validate_upload_size(upload, 100)


def test_missing_upload_size_is_rejected():
    with pytest.raises(ValueError, match="size is unavailable"):
        validate_upload_size(SimpleNamespace(), 100)
