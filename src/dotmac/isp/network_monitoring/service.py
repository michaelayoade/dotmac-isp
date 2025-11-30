"""
Network Monitoring Service (ISP-local stub)

This module provides a stub for NetworkMonitoringService.
For full functionality, the Platform package must be installed.

ISP deployments can either:
1. Use Platform as a runtime dependency for full monitoring capabilities
2. Implement ISP-specific monitoring service using ISP-local integrations
"""

from typing import TYPE_CHECKING, Any

import structlog

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from dotmac.isp.network_monitoring.schemas import (
        DeviceHealthResponse,
        DeviceMetricsResponse,
        DeviceType,
        NetworkAlertResponse,
        NetworkOverviewResponse,
        TrafficStatsResponse,
    )

logger = structlog.get_logger(__name__)


class NetworkMonitoringService:
    """
    ISP Network Monitoring Service stub.

    This is a minimal implementation. For full functionality including
    NetBox, VOLTHA, GenieACS, and Prometheus integration, install the
    Platform package and use dotmac.platform.network_monitoring.service.
    """

    def __init__(
        self,
        tenant_id: str,
        session: "AsyncSession | None" = None,
        **kwargs: Any,
    ):
        if not tenant_id:
            raise ValueError("tenant_id is required for NetworkMonitoringService")

        self.tenant_id = tenant_id
        self.session = session
        logger.info(
            "network_monitoring.stub_initialized",
            tenant_id=tenant_id,
            message="Using ISP stub service. Install Platform for full functionality.",
        )

    async def get_network_overview(self, tenant_id: str) -> "NetworkOverviewResponse":
        """Get network overview - stub returns empty overview."""
        from dotmac.isp.network_monitoring.schemas import NetworkOverviewResponse

        return NetworkOverviewResponse(tenant_id=tenant_id or self.tenant_id)

    async def get_all_devices(
        self,
        tenant_id: str,
        device_type: "DeviceType | None" = None,
    ) -> "list[DeviceHealthResponse]":
        """Get all devices - stub returns empty list."""
        return []

    async def get_device_health(
        self,
        device_id: str,
        device_type: "DeviceType | None",
        tenant_id: str,
    ) -> "DeviceHealthResponse | None":
        """Get device health - stub returns None."""
        return None

    async def get_device_metrics(
        self,
        device_id: str,
        device_type: "DeviceType | None",
        tenant_id: str,
    ) -> "DeviceMetricsResponse | None":
        """Get device metrics - stub returns None."""
        return None

    async def get_traffic_stats(
        self,
        device_id: str,
        device_type: "DeviceType | None",
        tenant_id: str,
    ) -> "TrafficStatsResponse | None":
        """Get traffic stats - stub returns None."""
        return None

    async def get_alerts(
        self,
        tenant_id: str,
        severity: Any = None,
        active_only: bool = True,
        device_id: str | None = None,
        limit: int = 100,
    ) -> "list[NetworkAlertResponse]":
        """Get alerts - stub returns empty list."""
        return []

    async def acknowledge_alert(
        self,
        alert_id: str,
        tenant_id: str,
        user_id: str,
        note: str | None = None,
    ) -> "NetworkAlertResponse | None":
        """Acknowledge alert - stub returns None."""
        return None

    async def create_alert_rule(
        self,
        tenant_id: str,
        name: str,
        description: str | None,
        device_type: Any,
        metric_name: str,
        condition: str,
        threshold: float,
        severity: Any,
        enabled: bool,
    ) -> dict[str, Any]:
        """Create alert rule - stub returns empty dict."""
        logger.warning(
            "network_monitoring.stub.create_alert_rule",
            tenant_id=tenant_id,
            message="Alert rules not supported in ISP stub. Install Platform for full functionality.",
        )
        return {}

    async def get_alert_rules(self, tenant_id: str) -> list[dict[str, Any]]:
        """Get alert rules - stub returns empty list."""
        return []


__all__ = ["NetworkMonitoringService"]
