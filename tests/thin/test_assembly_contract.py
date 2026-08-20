"""Canaries for the new thin assembly boundary.

The legacy ``src/dotmac/isp`` tree is an extraction source, not something the
replacement runtime may import.  These tests deliberately inspect the new
package only; ``test_legacy_boundary`` separately proves that this is a real,
non-empty boundary rather than an empty-directory exemption.
"""

from __future__ import annotations

import ast
from pathlib import Path

from dotmac_kernel.assembly import ProductAssemblySpec

from dotmac_isp.assembly import ASSEMBLY_NAME, build_spec
from dotmac_isp.config import FOREIGN_DATA_PLANE_URL_VARS, configuration_errors

REPO_ROOT = Path(__file__).resolve().parents[2]
THIN_SRC = REPO_ROOT / "src" / "dotmac_isp"
FORBIDDEN_IMPORT_ROOTS = frozenset(
    {
        "app",
        "dotmac",
        "dotmac_crm",
        "dotmac_erp",
        "dotmac_sub",
        "vendor_cp",
    }
)


def _instantiated_names(source: str) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            names.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            names.add(node.func.attr)
    return names


def _imported_roots(source: str) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def _source_files() -> list[Path]:
    return sorted(THIN_SRC.rglob("*.py"))


def test_spec_is_kernel_owned_and_declares_the_dedicated_first_profile() -> None:
    spec = build_spec()
    assert isinstance(spec, ProductAssemblySpec)
    assert spec.name == ASSEMBLY_NAME == "dotmac-isp"
    assert spec.tenancy == "single"
    assert spec.platform_surface_enabled is False
    assert spec.web_enabled is True


def test_walking_skeleton_composes_no_unreleased_domain_module() -> None:
    spec = build_spec()
    assert spec.modules == ()
    assert spec.module_planes == ()
    assert len(spec.packaged_static_dirs) == 1
    assert len(spec.stylesheets) == 1


def test_new_runtime_never_imports_a_product_or_legacy_data_plane() -> None:
    files = _source_files()
    assert files, "the thin-runtime import guard scanned no source files"
    findings = {
        str(path.relative_to(REPO_ROOT)): sorted(
            _imported_roots(path.read_text(encoding="utf-8")) & FORBIDDEN_IMPORT_ROOTS
        )
        for path in files
        if _imported_roots(path.read_text(encoding="utf-8")) & FORBIDDEN_IMPORT_ROOTS
    }
    assert findings == {}


def test_import_guard_detects_a_real_foreign_import() -> None:
    assert _imported_roots("from dotmac.isp.billing import service") == {"dotmac"}
    assert _imported_roots("import dotmac_sub.models") == {"dotmac_sub"}


def test_nothing_hand_builds_fastapi() -> None:
    findings = [
        str(path.relative_to(REPO_ROOT))
        for path in _source_files()
        if "FastAPI" in _instantiated_names(path.read_text(encoding="utf-8"))
    ]
    assert findings == []


def test_fastapi_guard_has_a_sensitivity_proof() -> None:
    assert "FastAPI" in _instantiated_names(
        "from fastapi import FastAPI\napp = FastAPI()"
    )


def test_main_is_only_a_create_app_adapter() -> None:
    main = (THIN_SRC / "main.py").read_text(encoding="utf-8")
    assert _instantiated_names(main) == {"build_spec", "create_app"}


def test_foreign_database_configuration_is_refused(monkeypatch) -> None:
    for variable in FOREIGN_DATA_PLANE_URL_VARS:
        monkeypatch.delenv(variable, raising=False)
    monkeypatch.delenv("MIGRATION_DATABASE_URL", raising=False)
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://app@db/isp")
    assert configuration_errors() == ()

    monkeypatch.setenv("DOTMAC_SUB_DATABASE_URL", "postgresql://foreign/sub")
    assert any("DOTMAC_SUB_DATABASE_URL" in error for error in configuration_errors())


def test_migration_authority_is_refused_by_the_online_runtime(monkeypatch) -> None:
    for variable in FOREIGN_DATA_PLANE_URL_VARS:
        monkeypatch.delenv(variable, raising=False)
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://app@db/isp")
    monkeypatch.setenv("MIGRATION_DATABASE_URL", "postgresql+psycopg://admin@db/isp")
    assert any("MIGRATION_DATABASE_URL" in error for error in configuration_errors())
