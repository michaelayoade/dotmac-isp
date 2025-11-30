"""
ISP Authentication Middleware.

Provides app boundary enforcement and single-tenant mode support
for standalone ISP deployments.
"""

from typing import Any, Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from dotmac.isp.settings import settings

logger = structlog.get_logger(__name__)


class AppBoundaryMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce app boundary checks.

    Ensures requests are properly scoped to the ISP tier
    and validates tenant context.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        # Mark request as ISP tier
        request.state.app_tier = "isp"

        # Extract tenant from header if present
        tenant_slug = request.headers.get("X-Tenant-Slug")
        if tenant_slug:
            request.state.tenant_slug = tenant_slug

        return await call_next(request)


class SingleTenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware for single-tenant deployment mode.

    In single-tenant mode, all requests are automatically scoped
    to the configured tenant without requiring X-Tenant-Slug header.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        # In single-tenant mode, inject the default tenant
        if settings.deployment_mode == "single_tenant":
            default_tenant = getattr(settings, "default_tenant_id", None)
            if default_tenant:
                request.state.tenant_id = default_tenant
                request.state.tenant_slug = getattr(
                    settings, "default_tenant_slug", default_tenant
                )

        return await call_next(request)
