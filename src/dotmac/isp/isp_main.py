"""
ISP Service Entrypoint.

Standalone entrypoint for the ISP operations service.
Mounts only ISP routes at /api/isp/v1.

Usage:
    uvicorn dotmac.isp.isp_main:app --host 0.0.0.0 --port 8001
"""

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.responses import Response

# Import from dotmac.shared (NOT dotmac.platform)
from dotmac.shared.core.exception_handlers import register_exception_handlers
from dotmac.shared.core.rate_limiting import get_limiter
from dotmac.shared.core.request_context import RequestContextMiddleware
from dotmac.shared.core.rls_middleware import RLSMiddleware
from dotmac.shared.audit import AuditContextMiddleware
from dotmac.shared.db import configure_database, init_db
from dotmac.shared.monitoring.error_middleware import (
    ErrorTrackingMiddleware,
    RequestMetricsMiddleware,
)
from dotmac.shared.monitoring.health_checks import HealthChecker
from dotmac.shared.redis_client import init_redis, shutdown_redis
from dotmac.shared.tenant import TenantMiddleware
from dotmac.shared.routers import ServiceScope, register_routers_for_scope

# Import ISP-specific settings and middleware
from dotmac.isp.settings import settings
from dotmac.isp.auth.middleware import (
    AppBoundaryMiddleware,
    SingleTenantMiddleware,
)
from dotmac.isp.platform_client.client import (
    PlatformClient,
    LicenseValidationError,
    ConfigSyncError,
)

logger = structlog.get_logger(__name__)

# Global platform client instance
_platform_client: PlatformClient | None = None
_periodic_sync_task: asyncio.Task[None] | None = None


def rate_limit_handler(request: Request, exc: Exception) -> Response:
    """Handle rate limit exceeded exceptions with proper typing."""
    return _rate_limit_exceeded_handler(request, exc)  # type: ignore[arg-type]


async def _init_database() -> None:
    """Initialize database with ISP settings."""
    configure_database(
        database_url=settings.database_url,
        async_database_url=settings.async_database_url,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        pool_recycle=settings.db_pool_recycle,
        pool_timeout=settings.db_pool_timeout,
        pool_pre_ping=True,
        echo=settings.db_echo,
    )
    init_db()


async def _init_platform_client() -> PlatformClient | None:
    """Initialize Platform client and perform startup checks.

    Returns PlatformClient on success, None if Platform integration is disabled.
    Raises on license validation failure (fail fast).
    """
    global _platform_client, _periodic_sync_task

    # Check if Platform integration is enabled
    platform_settings = settings.platform
    if not platform_settings.platform_url or not platform_settings.license_key:
        logger.warning(
            "isp_service.platform_disabled",
            reason="Missing PLATFORM_URL or ISP_LICENSE_KEY",
        )
        return None

    tenant_id = settings.tenant_id
    if not tenant_id:
        logger.warning(
            "isp_service.platform_disabled",
            reason="Missing TENANT_ID",
        )
        return None

    logger.info(
        "isp_service.platform_init",
        platform_url=platform_settings.platform_url,
        tenant_id=tenant_id,
    )

    # Create Platform client
    _platform_client = PlatformClient(
        platform_url=platform_settings.platform_url,
        tenant_id=tenant_id,
        license_key=platform_settings.license_key,
        service_secret=platform_settings.service_token,
        app_version=settings.app_version,
        timeout=platform_settings.timeout_seconds,
    )

    # Perform startup checks (validate license + sync config)
    try:
        await _platform_client.startup_check()
        logger.info(
            "isp_service.platform_startup_success",
            tenant_id=tenant_id,
            license_valid=True,
        )
    except LicenseValidationError as e:
        logger.error(
            "isp_service.license_invalid",
            tenant_id=tenant_id,
            error=str(e),
        )
        await _platform_client.close()
        _platform_client = None
        # Fail fast - don't start the service with invalid license
        raise RuntimeError(f"ISP startup failed: License validation failed - {e}")
    except ConfigSyncError as e:
        logger.error(
            "isp_service.config_sync_failed",
            tenant_id=tenant_id,
            error=str(e),
        )
        # Config sync failure is not fatal - we can continue with defaults
        logger.warning("isp_service.continuing_without_config_sync")
    except Exception as e:
        logger.error(
            "isp_service.platform_startup_failed",
            tenant_id=tenant_id,
            error=str(e),
        )
        await _platform_client.close()
        _platform_client = None
        raise RuntimeError(f"ISP startup failed: Platform connection failed - {e}")

    # Start periodic sync background task
    _periodic_sync_task = asyncio.create_task(
        _platform_client.periodic_sync(
            config_interval=platform_settings.config_sync_interval,
            metrics_interval=60,
            health_interval=30,
        )
    )
    logger.info("isp_service.periodic_sync_started")

    return _platform_client


async def _shutdown_platform_client() -> None:
    """Shutdown Platform client and cleanup."""
    global _platform_client, _periodic_sync_task

    if _periodic_sync_task is not None:
        _periodic_sync_task.cancel()
        try:
            await _periodic_sync_task
        except asyncio.CancelledError:
            pass
        _periodic_sync_task = None
        logger.info("isp_service.periodic_sync_stopped")

    if _platform_client is not None:
        await _platform_client.close()
        _platform_client = None
        logger.info("isp_service.platform_client_closed")


def get_platform_client() -> PlatformClient | None:
    """Get the global Platform client instance."""
    return _platform_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """ISP service lifecycle management."""
    logger.info("isp_service.starting", version=settings.app_version)

    # Initialize infrastructure
    await init_redis()
    await _init_database()

    # Initialize Platform client and validate license
    # This will fail fast if license is invalid
    await _init_platform_client()

    logger.info("isp_service.started")
    yield

    # Cleanup
    logger.info("isp_service.stopping")
    await _shutdown_platform_client()
    await shutdown_redis()
    logger.info("isp_service.stopped")


def create_isp_service() -> FastAPI:
    """
    Create the ISP operations service.

    This is a standalone service that handles:
    - Customer and subscriber management
    - Network operations (RADIUS, NetBox, GenieACS, VOLTHA)
    - Billing and revenue management
    - Service provisioning and lifecycle
    - Support and ticketing
    - Partner management

    Returns:
        FastAPI application instance
    """
    app = FastAPI(
        title="DotMac ISP Service",
        description="ISP operations and tenant management",
        version=settings.app_version,
        lifespan=lifespan,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
    )

    # Add middleware stack
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(ErrorTrackingMiddleware)
    app.add_middleware(RequestMetricsMiddleware)
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Tenant context middleware
    app.add_middleware(TenantMiddleware)

    # RLS enforcement
    app.add_middleware(RLSMiddleware)

    # Single-tenant mode support
    if settings.deployment_mode == "single_tenant":
        app.add_middleware(SingleTenantMiddleware)

    app.add_middleware(AuditContextMiddleware)
    app.add_middleware(AppBoundaryMiddleware)

    # CORS
    if settings.cors_enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=settings.cors_credentials,
            allow_methods=settings.cors_methods,
            allow_headers=settings.cors_headers,
            max_age=settings.cors_max_age,
        )

    # Rate limiting
    app.state.limiter = get_limiter()
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

    # Exception handlers
    register_exception_handlers(app)

    # Register ISP + SHARED routers at /api/isp/v1
    logger.info("isp_service.registering_routers")
    registered, failed = register_routers_for_scope(
        app,
        scope=ServiceScope.ISP,
        include_shared=True,
        prefix="/api/isp/v1",
        default_base_prefix="/admin",
    )
    logger.info(
        "isp_service.routers_registered",
        registered=registered,
        failed=failed,
    )

    # Health endpoints at root
    @app.get("/health")
    async def health_check() -> dict[str, Any]:
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": "isp",
            "version": settings.app_version,
        }

    @app.get("/health/live")
    async def liveness_check() -> dict[str, Any]:
        """Liveness check for Kubernetes."""
        return {
            "status": "alive",
            "service": "isp",
            "timestamp": datetime.now(UTC).isoformat(),
        }

    @app.get("/health/ready")
    async def readiness_check() -> dict[str, Any]:
        """Readiness check for Kubernetes."""
        checker = HealthChecker()
        summary = checker.get_summary()
        return {
            "status": "ready" if summary["healthy"] else "not ready",
            "service": "isp",
            "healthy": summary["healthy"],
            "services": summary["services"],
        }

    return app


# Application instance for uvicorn
app = create_isp_service()
