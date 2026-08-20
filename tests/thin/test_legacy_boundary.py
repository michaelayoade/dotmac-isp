"""The inherited application is frozen debt, not an unmonitored exclusion."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from scripts.check_legacy_baseline import snapshot, violations

REPO_ROOT = Path(__file__).resolve().parents[2]
BASELINE_PATH = REPO_ROOT / "docs" / "legacy-baseline.json"


def _baseline() -> dict[str, object]:
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def test_checked_in_legacy_baseline_matches_exactly() -> None:
    assert violations(_baseline(), snapshot(REPO_ROOT)) == []


def test_ratchet_detects_a_same_count_content_change() -> None:
    observed = snapshot(REPO_ROOT)
    changed = copy.deepcopy(observed)
    backend = changed["regions"]["legacy_backend"]  # type: ignore[index]
    backend["digest"] = "0" * 64  # type: ignore[index]
    errors = violations(observed, changed)
    assert any("legacy_backend.digest" in error for error in errors)


def test_ratchet_detects_an_unreviewed_reduction() -> None:
    observed = snapshot(REPO_ROOT)
    changed = copy.deepcopy(observed)
    node_modules = changed["regions"]["tracked_node_modules"]  # type: ignore[index]
    node_modules["count"] -= 1  # type: ignore[index,operator]
    errors = violations(observed, changed)
    assert any("tracked_node_modules.count" in error for error in errors)


def test_no_runtime_environment_file_is_tracked() -> None:
    observed = snapshot(REPO_ROOT)
    assert observed["tracked_runtime_env_files"] == []
