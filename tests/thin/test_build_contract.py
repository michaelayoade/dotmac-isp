"""The target build consumes exact releases and packages only the thin app."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = REPO_ROOT / "pyproject.toml"
FULL_REVISION = re.compile(r"^[0-9a-f]{40}$")
PINNED_ACTION = re.compile(r"uses:\s+[^\s@]+@[0-9a-f]{40}(?:\s|$)")


def _project() -> dict[str, object]:
    return tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))


def test_poetry_is_one_exact_build_input() -> None:
    poetry = _project()["tool"]["poetry"]  # type: ignore[index]
    assert poetry["requires-poetry"] == "2.4.1"  # type: ignore[index]
    assert poetry["packages"] == [  # type: ignore[index]
        {"include": "dotmac_isp", "from": "src"}
    ]


def test_starter_dependencies_are_exact_immutable_revisions() -> None:
    dependencies = _project()["tool"]["poetry"]["dependencies"]  # type: ignore[index]
    expected = {
        "dotmac-kernel": (
            "4cfdcd76739c9ad6c6dc249c1093849db7c3b752",
            "packages/dotmac-kernel",
        ),
        "dotmac-ui": (
            "042532d2c80ee7a56b14b71269d15459288312c2",
            "packages/dotmac-ui",
        ),
    }
    for name, (revision, subdirectory) in expected.items():
        declaration = dependencies[name]  # type: ignore[index]
        assert isinstance(declaration, dict)
        assert declaration.get("git") == (
            "https://github.com/michaelayoade/dotmac_starter_mt.git"
        )
        assert declaration.get("rev") == revision
        assert FULL_REVISION.fullmatch(str(declaration.get("rev")))
        assert declaration.get("subdirectory") == subdirectory
        assert "path" not in declaration
        assert declaration.get("develop") is not True


def test_container_runs_only_the_thin_entrypoint() -> None:
    dockerfile = (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert "dotmac_isp.main:app" in dockerfile
    assert "dotmac.isp" not in dockerfile
    assert "dotmac-shared" not in dockerfile
    assert "alembic upgrade" not in dockerfile


def test_default_compose_surface_builds_only_the_thin_candidate() -> None:
    compose = (REPO_ROOT / "compose.yaml").read_text(encoding="utf-8")
    assert "DATABASE_URL:?" in compose
    assert "dotmac.isp" not in compose
    assert "MIGRATION_DATABASE_URL" not in compose


def test_ci_actions_are_immutable_and_failures_are_not_ignored() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(
        encoding="utf-8"
    )
    uses = [line.strip() for line in workflow.splitlines() if "uses:" in line]
    assert uses
    assert all(PINNED_ACTION.search(line) for line in uses)
    assert "|| true" not in workflow
