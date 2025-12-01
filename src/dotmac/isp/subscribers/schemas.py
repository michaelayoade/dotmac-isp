"""
Subscriber Management Schemas.

Pydantic models for subscriber API requests and responses.
"""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from dotmac.isp.subscribers.models import PasswordHashingMethod, SubscriberStatus
from dotmac.isp.services.lifecycle.models import ServiceType


# =============================================================================
# Enums for API
# =============================================================================


class SubscriberStatusFilter(str, Enum):
    """Filter options for subscriber status queries."""

    ALL = "all"
    ACTIVE = "active"
    PENDING = "pending"
    SUSPENDED = "suspended"
    DISCONNECTED = "disconnected"
    TERMINATED = "terminated"
    QUARANTINED = "quarantined"


# =============================================================================
# Base Schemas
# =============================================================================


class SubscriberBase(BaseModel):
    """Base subscriber fields."""

    username: str = Field(..., min_length=3, max_length=64, description="RADIUS username")
    full_name: str | None = Field(None, max_length=255, description="Subscriber full name")
    email: EmailStr | None = Field(None, description="Contact email")
    phone_number: str | None = Field(None, max_length=32, description="Contact phone")
    subscriber_number: str = Field(
        default="", max_length=50, description="Human-readable subscriber ID"
    )


class SubscriberNetworkConfig(BaseModel):
    """Network configuration for a subscriber."""

    bandwidth_profile_id: str | None = Field(None, description="Bandwidth/QoS profile ID")
    download_speed_kbps: int | None = Field(None, ge=0, description="Download speed in Kbps")
    upload_speed_kbps: int | None = Field(None, ge=0, description="Upload speed in Kbps")
    static_ipv4: str | None = Field(None, description="Static IPv4 address")
    ipv6_prefix: str | None = Field(None, description="IPv6 prefix delegation")
    vlan_id: int | None = Field(None, ge=1, le=4094, description="VLAN assignment")
    nas_identifier: str | None = Field(None, max_length=128, description="NAS device identifier")


class SubscriberDeviceConfig(BaseModel):
    """Device configuration for a subscriber."""

    onu_serial: str | None = Field(None, max_length=50, description="ONU serial number")
    cpe_mac_address: str | None = Field(None, max_length=17, description="CPE MAC address")
    device_metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional device info"
    )


class SubscriberLocationConfig(BaseModel):
    """Service location configuration."""

    service_address: str | None = Field(None, max_length=500, description="Full service address")
    service_coordinates: dict[str, Any] = Field(
        default_factory=dict, description="GPS coordinates {lat, lon}"
    )
    site_id: str | None = Field(None, max_length=100, description="Network site/POP identifier")


class SubscriberSessionConfig(BaseModel):
    """RADIUS session configuration."""

    session_timeout: int | None = Field(
        None, ge=0, description="Max session duration in seconds"
    )
    idle_timeout: int | None = Field(None, ge=0, description="Idle timeout in seconds")
    simultaneous_use: int = Field(
        default=1, ge=1, description="Max concurrent sessions allowed"
    )


# =============================================================================
# Create/Update Schemas
# =============================================================================


class SubscriberCreate(SubscriberBase):
    """Schema for creating a new subscriber."""

    model_config = ConfigDict(from_attributes=True)

    # Required fields
    password: str | None = Field(
        None,
        min_length=8,
        max_length=128,
        description="RADIUS password (auto-generated if not provided)",
    )
    password_hash_method: PasswordHashingMethod = Field(
        default=PasswordHashingMethod.SHA256, description="Password hashing method"
    )

    # Optional associations
    customer_id: UUID | None = Field(None, description="Link to billing customer")
    user_id: UUID | None = Field(None, description="Link to portal user account")

    # Service configuration
    service_type: ServiceType = Field(
        default=ServiceType.FIBER_INTERNET, description="Type of service"
    )
    status: SubscriberStatus = Field(
        default=SubscriberStatus.PENDING, description="Initial status"
    )

    # Network configuration
    network: SubscriberNetworkConfig = Field(
        default_factory=SubscriberNetworkConfig, description="Network settings"
    )

    # Device configuration
    device: SubscriberDeviceConfig = Field(
        default_factory=SubscriberDeviceConfig, description="Device settings"
    )

    # Location configuration
    location: SubscriberLocationConfig = Field(
        default_factory=SubscriberLocationConfig, description="Location settings"
    )

    # Session configuration
    session: SubscriberSessionConfig = Field(
        default_factory=SubscriberSessionConfig, description="RADIUS session settings"
    )

    # Metadata
    metadata_: dict[str, Any] = Field(
        default_factory=dict, alias="metadata", description="Custom metadata"
    )
    notes: str | None = Field(None, description="Internal notes")

    # Auto-activate subscriber and create RADIUS credentials
    auto_activate: bool = Field(
        default=False, description="Automatically activate and create RADIUS credentials"
    )


class SubscriberUpdate(BaseModel):
    """Schema for updating an existing subscriber."""

    model_config = ConfigDict(from_attributes=True)

    # Basic info (all optional for partial updates)
    username: str | None = Field(None, min_length=3, max_length=64)
    full_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    subscriber_number: str | None = None

    # Associations
    customer_id: UUID | None = None
    user_id: UUID | None = None

    # Service configuration
    service_type: ServiceType | None = None
    status: SubscriberStatus | None = None

    # Network configuration
    bandwidth_profile_id: str | None = None
    download_speed_kbps: int | None = None
    upload_speed_kbps: int | None = None
    static_ipv4: str | None = None
    ipv6_prefix: str | None = None
    vlan_id: int | None = None
    nas_identifier: str | None = None

    # Device configuration
    onu_serial: str | None = None
    cpe_mac_address: str | None = None
    device_metadata: dict[str, Any] | None = None

    # Location configuration
    service_address: str | None = None
    service_coordinates: dict[str, Any] | None = None
    site_id: str | None = None

    # Session configuration
    session_timeout: int | None = None
    idle_timeout: int | None = None
    simultaneous_use: int | None = None

    # Metadata
    metadata_: dict[str, Any] | None = Field(None, alias="metadata")
    notes: str | None = None


class SubscriberPasswordChange(BaseModel):
    """Schema for changing subscriber password."""

    new_password: str | None = Field(
        None, min_length=8, max_length=128, description="New password (auto-generated if empty)"
    )
    hash_method: PasswordHashingMethod = Field(
        default=PasswordHashingMethod.SHA256, description="Hashing method"
    )
    update_radius: bool = Field(
        default=True, description="Update RADIUS credentials immediately"
    )


class SubscriberStatusChange(BaseModel):
    """Schema for changing subscriber status."""

    status: SubscriberStatus = Field(..., description="New status")
    reason: str | None = Field(None, max_length=500, description="Reason for status change")
    disconnect_active_sessions: bool = Field(
        default=True, description="Disconnect active RADIUS sessions on suspend/terminate"
    )


class SubscriberActivate(BaseModel):
    """Schema for activating a pending subscriber."""

    create_radius_credentials: bool = Field(
        default=True, description="Create RADIUS authentication entries"
    )
    send_welcome_notification: bool = Field(
        default=False, description="Send welcome email/SMS to subscriber"
    )


# =============================================================================
# Response Schemas
# =============================================================================


class SubscriberResponse(BaseModel):
    """Full subscriber response."""

    model_config = ConfigDict(from_attributes=True)

    # Identity
    id: str
    tenant_id: str
    username: str
    subscriber_number: str
    full_name: str | None
    email: str | None
    phone_number: str | None

    # Associations
    customer_id: UUID | None
    user_id: UUID | None

    # Status
    status: SubscriberStatus
    service_type: ServiceType

    # Network
    bandwidth_profile_id: str | None
    download_speed_kbps: int | None
    upload_speed_kbps: int | None
    static_ipv4: str | None
    ipv6_prefix: str | None
    vlan_id: int | None
    nas_identifier: str | None

    # Device
    onu_serial: str | None
    cpe_mac_address: str | None
    device_metadata: dict[str, Any]

    # Location
    service_address: str | None
    service_coordinates: dict[str, Any]
    site_id: str | None

    # Session
    session_timeout: int | None
    idle_timeout: int | None
    simultaneous_use: int

    # Dates
    activation_date: datetime | None
    suspension_date: datetime | None
    termination_date: datetime | None
    last_online: datetime | None
    created_at: datetime
    updated_at: datetime

    # Usage stats
    total_sessions: int
    total_upload_bytes: int
    total_download_bytes: int

    # External refs
    netbox_ip_id: int | None
    voltha_onu_id: str | None
    genieacs_device_id: str | None

    # Meta
    metadata_: dict[str, Any] = Field(alias="metadata")
    notes: str | None

    # Computed
    is_active: bool
    is_password_secure: bool
    display_name: str
    total_bytes: int


class SubscriberSummary(BaseModel):
    """Lightweight subscriber summary for lists."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    subscriber_number: str
    full_name: str | None
    email: str | None
    status: SubscriberStatus
    service_type: ServiceType
    download_speed_kbps: int | None
    upload_speed_kbps: int | None
    last_online: datetime | None
    created_at: datetime
    is_active: bool


class SubscriberList(BaseModel):
    """Paginated subscriber list response."""

    items: list[SubscriberSummary]
    total: int
    page: int
    page_size: int
    pages: int


class SubscriberPasswordResponse(BaseModel):
    """Response after password change/generation."""

    subscriber_id: str
    username: str
    new_password: str = Field(..., description="The new password (only shown once)")
    hash_method: str
    radius_updated: bool


class SubscriberActivationResponse(BaseModel):
    """Response after subscriber activation."""

    subscriber_id: str
    username: str
    status: SubscriberStatus
    radius_credentials_created: bool
    password: str | None = Field(
        None, description="Generated password (only if newly created)"
    )
    activation_date: datetime


# =============================================================================
# Query/Filter Schemas
# =============================================================================


class SubscriberQuery(BaseModel):
    """Query parameters for subscriber search."""

    # Text search
    search: str | None = Field(
        None, description="Search username, subscriber_number, full_name, email"
    )

    # Filters
    status: SubscriberStatusFilter = Field(
        default=SubscriberStatusFilter.ALL, description="Filter by status"
    )
    service_type: ServiceType | None = Field(None, description="Filter by service type")
    customer_id: UUID | None = Field(None, description="Filter by customer")
    site_id: str | None = Field(None, description="Filter by site/POP")
    nas_identifier: str | None = Field(None, description="Filter by NAS")

    # Date filters
    created_after: datetime | None = None
    created_before: datetime | None = None
    last_online_after: datetime | None = None

    # Pagination
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    # Sorting
    sort_by: str = Field(default="created_at", description="Sort field")
    sort_desc: bool = Field(default=True, description="Sort descending")


class SubscriberStats(BaseModel):
    """Subscriber statistics for dashboard."""

    total: int
    active: int
    pending: int
    suspended: int
    terminated: int

    # By service type
    by_service_type: dict[str, int]

    # Recent activity
    new_last_7_days: int
    new_last_30_days: int
    online_now: int
