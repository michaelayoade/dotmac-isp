"""
Models for Platform communication.

These mirror the Platform API models for type safety.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict


class LicenseInfo(BaseModel):
    """License information from Platform."""

    model_config = ConfigDict()

    license_key: str
    tenant_id: str
    tenant_name: str
    is_valid: bool
    expires_at: datetime | None
    features: dict[str, Any]
    max_subscribers: int | None
    current_subscribers: int | None


class TenantConfig(BaseModel):
    """Tenant configuration from Platform."""

    model_config = ConfigDict()

    tenant_id: str
    tenant_name: str
    config_version: str
    updated_at: datetime

    radius: dict[str, Any]
    billing: dict[str, Any]
    features: dict[str, bool]
    branding: dict[str, Any]


class UsageMetrics(BaseModel):
    """Usage metrics to report to Platform."""

    model_config = ConfigDict()

    tenant_id: str
    reported_at: datetime

    # Subscriber metrics
    active_subscribers: int
    total_subscribers: int
    new_subscribers_today: int
    churned_subscribers_today: int

    # Session metrics
    active_sessions: int
    sessions_today: int
    total_data_usage_mb: float

    # Infrastructure metrics
    active_nas_devices: int
    active_olts: int
    active_onts: int

    # Financial metrics (optional)
    revenue_today: float | None = None
    outstanding_invoices: float | None = None


class HealthReport(BaseModel):
    """Health status to report to Platform."""

    model_config = ConfigDict()

    tenant_id: str
    reported_at: datetime
    status: str  # "healthy", "degraded", "unhealthy"

    api_status: str
    radius_status: str
    database_status: str
    redis_status: str

    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float

    app_version: str
    config_version: str


class EventType(str, Enum):
    """Types of events ISP can send to Platform."""

    SUBSCRIBER_CREATED = "subscriber.created"
    SUBSCRIBER_ACTIVATED = "subscriber.activated"
    SUBSCRIBER_SUSPENDED = "subscriber.suspended"
    SUBSCRIBER_TERMINATED = "subscriber.terminated"
    SUBSCRIBER_UPGRADED = "subscriber.upgraded"
    SUBSCRIBER_DOWNGRADED = "subscriber.downgraded"

    PAYMENT_RECEIVED = "payment.received"
    PAYMENT_FAILED = "payment.failed"
    INVOICE_CREATED = "invoice.created"
    INVOICE_OVERDUE = "invoice.overdue"

    TICKET_CREATED = "ticket.created"
    TICKET_ESCALATED = "ticket.escalated"
    TICKET_RESOLVED = "ticket.resolved"

    NAS_ONLINE = "nas.online"
    NAS_OFFLINE = "nas.offline"
    OLT_ALARM = "olt.alarm"
    ONT_ALARM = "ont.alarm"

    SESSION_STARTED = "session.started"
    SESSION_ENDED = "session.ended"
    SESSION_TERMINATED = "session.terminated"


class WebhookEvent(BaseModel):
    """Event to send to Platform."""

    model_config = ConfigDict()

    event_id: str
    event_type: EventType
    tenant_id: str
    occurred_at: datetime
    payload: dict[str, Any]
    metadata: dict[str, Any] | None = None
