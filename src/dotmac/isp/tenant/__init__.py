"""
ISP Tenant Module.

In the ISP application, each instance is tied to a single tenant.
The tenant ID comes from the ISP settings (configured per-instance).
"""

from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..settings import Settings

# Context variable for request-scoped tenant ID
_tenant_context: ContextVar[str | None] = ContextVar("tenant_id", default=None)


def get_current_tenant_id() -> str | None:
    """Get current tenant ID.

    In ISP, this returns:
    1. Request context tenant ID (if set by middleware)
    2. Default tenant from settings (single-tenant mode)
    """
    tenant_id = _tenant_context.get()
    if tenant_id:
        return tenant_id

    # Fall back to settings default
    from ..settings import settings
    return settings.tenant_id or settings.default_tenant_id


def set_current_tenant_id(tenant_id: str | None) -> None:
    """Set current tenant ID in request context."""
    _tenant_context.set(tenant_id)


def require_tenant_id() -> str:
    """Get current tenant ID, raising if not set."""
    tenant_id = get_current_tenant_id()
    if not tenant_id:
        raise ValueError("No tenant ID in context")
    return tenant_id


__all__ = [
    "get_current_tenant_id",
    "set_current_tenant_id",
    "require_tenant_id",
]
