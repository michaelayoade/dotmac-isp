"""Assembly-owned startup refusals; values remain in the environment."""

from __future__ import annotations

import os
from collections.abc import Sequence
from typing import Final

DATABASE_URL_VAR: Final[str] = "DATABASE_URL"
MIGRATION_DATABASE_URL_VAR: Final[str] = "MIGRATION_DATABASE_URL"

FOREIGN_DATA_PLANE_URL_VARS: Final[tuple[str, ...]] = (
    "CRM_DATABASE_URL",
    "DOTMAC_CRM_DATABASE_URL",
    "DOTMAC_ERP_DATABASE_URL",
    "DOTMAC_SUB_DATABASE_URL",
    "ERP_DATABASE_URL",
    "SUB_DATABASE_URL",
    "VENDOR_CP_DATABASE_URL",
)


def configuration_errors() -> Sequence[str]:
    """Return configuration defects without quoting any configured value."""
    errors: list[str] = []
    if not os.environ.get(DATABASE_URL_VAR, "").strip():
        errors.append(
            f"{DATABASE_URL_VAR} is unset. Configure the Dotmac ISP online "
            "role's independent database DSN."
        )
    if os.environ.get(MIGRATION_DATABASE_URL_VAR, "").strip():
        errors.append(
            f"{MIGRATION_DATABASE_URL_VAR} is installed in the online runtime. "
            "Keep migration authority in the separate deploy process."
        )
    for variable in FOREIGN_DATA_PLANE_URL_VARS:
        if os.environ.get(variable, "").strip():
            errors.append(
                f"{variable} is set. Dotmac ISP never reads another "
                "application's database; use a versioned API or webhook."
            )
    return tuple(errors)


__all__ = [
    "DATABASE_URL_VAR",
    "FOREIGN_DATA_PLANE_URL_VARS",
    "MIGRATION_DATABASE_URL_VAR",
    "configuration_errors",
]
