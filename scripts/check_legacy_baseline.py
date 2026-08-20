#!/usr/bin/env python3
"""Two-directional ratchet for inherited, non-authoritative repository debt."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import cast

JsonObject = dict[str, object]
ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "docs" / "legacy-baseline.json"


def _tracked_entries(root: Path) -> list[tuple[str, str]]:
    result = subprocess.run(
        ["git", "ls-files", "-s", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    entries: list[tuple[str, str]] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        metadata, raw_path = raw.split(b"\t", 1)
        _, digest, _ = metadata.decode("ascii").split(" ")
        path = raw_path.decode("utf-8")
        if (root / path).is_file():
            entries.append((path, digest))
    return entries


def _region(entries: list[tuple[str, str]]) -> JsonObject:
    digest = hashlib.sha256()
    for path, blob in sorted(entries):
        digest.update(path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(blob.encode("ascii"))
        digest.update(b"\n")
    return {"count": len(entries), "digest": digest.hexdigest()}


def snapshot(root: Path) -> JsonObject:
    entries = _tracked_entries(root)
    node_modules = [entry for entry in entries if "/node_modules/" in entry[0]]
    frontend = [
        entry
        for entry in entries
        if entry[0].startswith("frontend/")
        and "/node_modules/" not in entry[0]
        and entry[0] != "frontend/apps/isp-ops-app/.env.local"
    ]
    runtime_env = sorted(
        path
        for path, _ in entries
        if Path(path).name.startswith(".env") and not path.endswith(".example")
    )
    return {
        "schema_version": 1,
        "regions": {
            "legacy_backend": _region(
                [entry for entry in entries if entry[0].startswith("src/dotmac/")]
            ),
            "legacy_tests": _region(
                [
                    entry
                    for entry in entries
                    if entry[0].startswith("tests/")
                    and not entry[0].startswith("tests/thin/")
                ]
            ),
            "legacy_frontend": _region(frontend),
            "tracked_node_modules": _region(node_modules),
        },
        "tracked_runtime_env_files": runtime_env,
    }


def violations(expected: JsonObject, observed: JsonObject) -> list[str]:
    errors: list[str] = []
    if expected.keys() != observed.keys():
        errors.append("baseline top-level fields changed")
        return errors
    if expected.get("schema_version") != 1 or observed.get("schema_version") != 1:
        errors.append("legacy baseline schema_version must be 1")
    expected_regions = cast(JsonObject, expected.get("regions"))
    observed_regions = cast(JsonObject, observed.get("regions"))
    if expected_regions.keys() != observed_regions.keys():
        errors.append("legacy baseline region set changed")
        return errors
    for name in sorted(expected_regions):
        expected_region = cast(JsonObject, expected_regions[name])
        observed_region = cast(JsonObject, observed_regions[name])
        for field in ("count", "digest"):
            if expected_region.get(field) != observed_region.get(field):
                errors.append(
                    f"{name}.{field}: expected {expected_region.get(field)!r}, "
                    f"observed {observed_region.get(field)!r}; update the baseline "
                    "in the same reviewed retirement/exception change"
                )
    if expected.get("tracked_runtime_env_files") != observed.get(
        "tracked_runtime_env_files"
    ):
        errors.append("tracked_runtime_env_files changed")
    return errors


def main() -> int:
    expected = cast(JsonObject, json.loads(BASELINE.read_text(encoding="utf-8")))
    errors = violations(expected, snapshot(ROOT))
    if errors:
        for error in errors:
            print(f"error: {error}")
        return 1
    print("Legacy containment baseline matches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
