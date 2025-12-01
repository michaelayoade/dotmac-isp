"""
Platform Client - HTTP client for communicating with Platform API.

This client handles all communication between ISP and Platform:
- License validation
- Configuration sync
- Metrics reporting
- Event webhooks
"""

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any

import httpx

from dotmac.shared.service_auth import ServiceAuthenticator

from .models import (
    EventType,
    HealthReport,
    LicenseInfo,
    TenantConfig,
    UsageMetrics,
    WebhookEvent,
)

logger = logging.getLogger(__name__)


class PlatformClientError(Exception):
    """Base exception for Platform client errors."""

    pass


class LicenseValidationError(PlatformClientError):
    """License validation failed."""

    pass


class ConfigSyncError(PlatformClientError):
    """Configuration sync failed."""

    pass


class PlatformClient:
    """HTTP client for Platform API communication.

    Usage:
        client = PlatformClient(
            platform_url="https://platform.dotmac.io",
            tenant_id="tenant-123",
            license_key="lic_abc123",
            service_secret="shared-secret",
        )

        # Validate license on startup
        license_info = await client.validate_license()

        # Sync configuration
        config = await client.sync_config()

        # Report metrics periodically
        await client.report_metrics(metrics)

        # Send events
        await client.send_event(event)
    """

    def __init__(
        self,
        platform_url: str,
        tenant_id: str,
        license_key: str,
        service_secret: str,
        app_version: str = "1.0.0",
        timeout: float = 30.0,
    ):
        self.platform_url = platform_url.rstrip("/")
        self.tenant_id = tenant_id
        self.license_key = license_key
        self.app_version = app_version
        self.timeout = timeout

        # Initialize service authenticator
        self._auth = ServiceAuthenticator(service_secret)

        # HTTP client (created lazily)
        self._client: httpx.AsyncClient | None = None

        # Cached values
        self._license_info: LicenseInfo | None = None
        self._config: TenantConfig | None = None
        self._config_version: str | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.platform_url,
                timeout=self.timeout,
                headers=self._get_headers(),
            )
        return self._client

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with service token."""
        token = self._auth.create_service_token(
            service_id=f"isp-{self.tenant_id}",
            service_type="isp",
            tenant_id=self.tenant_id,
            permissions=["license:read", "config:read", "metrics:write", "events:write"],
        )
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-ISP-Version": self.app_version,
            "X-Tenant-ID": self.tenant_id,
        }

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self) -> "PlatformClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    # -------------------------------------------------------------------------
    # License API
    # -------------------------------------------------------------------------

    async def validate_license(self) -> LicenseInfo:
        """Validate the ISP license with Platform.

        Should be called on startup to ensure the license is valid.

        Returns:
            LicenseInfo with license details

        Raises:
            LicenseValidationError: If license is invalid or expired
        """
        client = await self._get_client()

        try:
            response = await client.post(
                "/api/platform/v1/service-api/license/validate",
                json={
                    "license_key": self.license_key,
                    "isp_instance_id": f"isp-{self.tenant_id}",
                    "version": self.app_version,
                },
                headers=self._get_headers(),
            )
            response.raise_for_status()

            data = response.json()
            if not data.get("valid"):
                raise LicenseValidationError(data.get("message", "License invalid"))

            self._license_info = LicenseInfo(**data["license_info"])
            self._config_version = data.get("config_hash")

            logger.info(
                "License validated successfully",
                extra={
                    "tenant_id": self.tenant_id,
                    "expires_at": self._license_info.expires_at,
                },
            )

            return self._license_info

        except httpx.HTTPStatusError as e:
            logger.error(f"License validation failed: {e.response.text}")
            raise LicenseValidationError(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"License validation request failed: {e}")
            raise LicenseValidationError(f"Request error: {e}")

    async def get_license_info(self) -> LicenseInfo:
        """Get cached license info or fetch from Platform."""
        if self._license_info is None:
            return await self.validate_license()
        return self._license_info

    # -------------------------------------------------------------------------
    # Config API
    # -------------------------------------------------------------------------

    async def sync_config(self, force: bool = False) -> TenantConfig:
        """Sync configuration from Platform.

        Args:
            force: If True, always fetch full config even if unchanged

        Returns:
            TenantConfig with current configuration

        Raises:
            ConfigSyncError: If config sync fails
        """
        client = await self._get_client()

        try:
            response = await client.post(
                f"/api/platform/v1/service-api/config/{self.tenant_id}/sync",
                json={"current_version": None if force else self._config_version},
                headers=self._get_headers(),
            )
            response.raise_for_status()

            data = response.json()

            if data.get("needs_update") and data.get("config"):
                self._config = TenantConfig(**data["config"])
                self._config_version = self._config.config_version
                logger.info(
                    "Configuration updated",
                    extra={
                        "tenant_id": self.tenant_id,
                        "version": self._config_version,
                    },
                )
            elif self._config is None:
                # First sync, must have config
                raise ConfigSyncError("No configuration received")

            return self._config

        except httpx.HTTPStatusError as e:
            logger.error(f"Config sync failed: {e.response.text}")
            raise ConfigSyncError(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Config sync request failed: {e}")
            raise ConfigSyncError(f"Request error: {e}")

    async def get_config(self) -> TenantConfig:
        """Get cached config or sync from Platform."""
        if self._config is None:
            return await self.sync_config()
        return self._config

    # -------------------------------------------------------------------------
    # Metrics API
    # -------------------------------------------------------------------------

    async def report_metrics(self, metrics: UsageMetrics) -> dict[str, Any]:
        """Report usage metrics to Platform.

        Should be called periodically (e.g., every 5 minutes).

        Args:
            metrics: Usage metrics to report

        Returns:
            Response from Platform including any warnings
        """
        client = await self._get_client()

        try:
            response = await client.post(
                "/api/platform/v1/service-api/metrics/report",
                json={"metrics": metrics.model_dump(mode="json")},
                headers=self._get_headers(),
            )
            response.raise_for_status()

            data = response.json()

            if data.get("warnings"):
                for warning in data["warnings"]:
                    logger.warning(f"Platform warning: {warning}")

            return data

        except httpx.HTTPError as e:
            logger.error(f"Metrics report failed: {e}")
            return {"received": False, "error": str(e)}

    async def report_health(self, report: HealthReport) -> dict[str, str]:
        """Report health status to Platform.

        Should be called frequently (e.g., every minute).
        """
        client = await self._get_client()

        try:
            response = await client.post(
                "/api/platform/v1/service-api/metrics/health",
                json=report.model_dump(mode="json"),
                headers=self._get_headers(),
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Health report failed: {e}")
            return {"status": "error", "message": str(e)}

    # -------------------------------------------------------------------------
    # Events API
    # -------------------------------------------------------------------------

    async def send_event(self, event: WebhookEvent) -> dict[str, str]:
        """Send a single event to Platform.

        For real-time notifications of important events.
        """
        client = await self._get_client()

        try:
            response = await client.post(
                "/api/platform/v1/service-api/events/webhook",
                json=event.model_dump(mode="json"),
                headers=self._get_headers(),
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Event send failed: {e}")
            return {"status": "error", "message": str(e)}

    async def send_events_batch(self, events: list[WebhookEvent]) -> dict[str, Any]:
        """Send a batch of events to Platform.

        More efficient for bulk event transmission.
        """
        client = await self._get_client()

        try:
            response = await client.post(
                "/api/platform/v1/service-api/events/webhook/batch",
                json={"events": [e.model_dump(mode="json") for e in events]},
                headers=self._get_headers(),
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Batch event send failed: {e}")
            return {"received": 0, "processed": 0, "failed": len(events), "error": str(e)}

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------

    async def startup_check(self) -> bool:
        """Perform all startup checks.

        Call this on ISP application startup to:
        1. Validate license
        2. Sync configuration

        Returns:
            True if all checks pass

        Raises:
            LicenseValidationError: If license is invalid
            ConfigSyncError: If config sync fails
        """
        logger.info("Performing startup checks with Platform...")

        # Validate license first
        license_info = await self.validate_license()
        if not license_info.is_valid:
            raise LicenseValidationError("License is invalid or expired")

        # Sync configuration
        await self.sync_config(force=True)

        logger.info("Startup checks completed successfully")
        return True

    async def periodic_sync(
        self,
        config_interval: int = 300,  # 5 minutes
        metrics_interval: int = 60,  # 1 minute
        health_interval: int = 30,  # 30 seconds
    ) -> None:
        """Run periodic sync tasks.

        This should be run as a background task.
        """
        last_config_sync = 0.0
        last_metrics_report = 0.0
        last_health_report = 0.0

        while True:
            now = datetime.now(UTC).timestamp()

            # Config sync
            if now - last_config_sync >= config_interval:
                try:
                    await self.sync_config()
                    last_config_sync = now
                except Exception as e:
                    logger.error(f"Periodic config sync failed: {e}")

            # Metrics report
            if now - last_metrics_report >= metrics_interval:
                try:
                    # TODO: Collect actual metrics
                    metrics = UsageMetrics(
                        tenant_id=self.tenant_id,
                        reported_at=datetime.now(UTC),
                        active_subscribers=0,
                        total_subscribers=0,
                        new_subscribers_today=0,
                        churned_subscribers_today=0,
                        active_sessions=0,
                        sessions_today=0,
                        total_data_usage_mb=0,
                        active_nas_devices=0,
                        active_olts=0,
                        active_onts=0,
                    )
                    await self.report_metrics(metrics)
                    last_metrics_report = now
                except Exception as e:
                    logger.error(f"Periodic metrics report failed: {e}")

            # Health report
            if now - last_health_report >= health_interval:
                try:
                    # TODO: Collect actual health status
                    health = HealthReport(
                        tenant_id=self.tenant_id,
                        reported_at=datetime.now(UTC),
                        status="healthy",
                        api_status="healthy",
                        radius_status="healthy",
                        database_status="healthy",
                        redis_status="healthy",
                        cpu_usage_percent=0,
                        memory_usage_percent=0,
                        disk_usage_percent=0,
                        app_version=self.app_version,
                        config_version=self._config_version or "unknown",
                    )
                    await self.report_health(health)
                    last_health_report = now
                except Exception as e:
                    logger.error(f"Periodic health report failed: {e}")

            await asyncio.sleep(10)  # Check every 10 seconds
