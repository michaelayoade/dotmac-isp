"""
Platform Client - ISP's interface to communicate with Platform.

This module provides:
- License validation on startup
- Configuration sync
- Metrics reporting
- Event webhooks
"""

from .client import PlatformClient
from .models import (
    LicenseInfo,
    TenantConfig,
    UsageMetrics,
    HealthReport,
    WebhookEvent,
    EventType,
)

__all__ = [
    "PlatformClient",
    "LicenseInfo",
    "TenantConfig",
    "UsageMetrics",
    "HealthReport",
    "WebhookEvent",
    "EventType",
]
