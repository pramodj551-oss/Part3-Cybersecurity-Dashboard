"""Minimal structured runtime observability for production events."""

from __future__ import annotations

import json
import logging
import time
from typing import Any

LOGGER = logging.getLogger("part3.runtime")


def _safe_event(event: str, status: str, **fields: Any) -> dict[str, Any]:
    """Build a bounded, JSON-serializable event without exception details."""
    allowed = {
        "duration_ms",
        "rows",
        "columns",
        "prediction_count",
        "error_category",
    }
    payload = {
        "event": event,
        "status": status,
        "timestamp_unix_ms": int(time.time() * 1000),
    }
    for key, value in fields.items():
        if key in allowed and isinstance(value, (bool, int, float, str)):
            payload[key] = value
    return payload


def emit_event(event: str, status: str, **fields: Any) -> dict[str, Any]:
    """Emit one structured JSON runtime event and return the emitted payload."""
    payload = _safe_event(event, status, **fields)
    LOGGER.info(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return payload


def start_timer() -> float:
    """Return a monotonic start time for runtime duration measurement."""
    return time.monotonic()


def elapsed_ms(started: float) -> float:
    """Return elapsed duration in milliseconds."""
    return round((time.monotonic() - started) * 1000, 3)
