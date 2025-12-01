"""
ISP Application Settings.

Configuration for the ISP operations application, loaded from environment variables.
This is separate from Platform settings to allow independent deployment.
"""

from __future__ import annotations

import os
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Application environment."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class ServiceEndpointSettings(BaseModel):
    """External service endpoint configuration."""

    model_config = ConfigDict()

    url: str | None = Field(None, description="Base URL for the service endpoint")
    username: str | None = Field(None, description="Optional username for basic auth")
    password: str | None = Field(None, description="Optional password for basic auth")
    api_token: str | None = Field(None, description="Optional API token")
    verify_ssl: bool = Field(True, description="Verify SSL certificates")
    timeout_seconds: float = Field(30.0, ge=1.0, description="HTTP timeout in seconds")
    max_retries: int = Field(2, ge=0, description="Number of automatic retries")
    extras: dict[str, Any] = Field(default_factory=dict, description="Additional config values")


class PlatformConnectionSettings(BaseModel):
    """Settings for connecting to the Platform control plane."""

    model_config = ConfigDict()

    platform_url: str = Field(
        default_factory=lambda: os.getenv("PLATFORM_URL", "http://localhost:8000"),
        description="Platform API base URL",
    )
    service_token: str = Field(
        default_factory=lambda: os.getenv("PLATFORM_SERVICE_TOKEN", ""),
        description="Service authentication token for Platform API",
    )
    license_key: str = Field(
        default_factory=lambda: os.getenv("ISP_LICENSE_KEY", ""),
        description="ISP license key for Platform validation",
    )
    verify_ssl: bool = Field(
        default_factory=lambda: os.getenv("PLATFORM_VERIFY_SSL", "true").lower()
        not in {"false", "0"},
        description="Verify Platform SSL certificate",
    )
    timeout_seconds: float = Field(
        default_factory=lambda: float(os.getenv("PLATFORM_TIMEOUT_SECONDS", "30")),
        description="Platform API timeout in seconds",
    )
    config_sync_interval: int = Field(
        default_factory=lambda: int(os.getenv("CONFIG_SYNC_INTERVAL", "300")),
        description="Configuration sync interval in seconds",
    )


class RADIUSSettings(BaseModel):
    """RADIUS server configuration for CoA/DM operations."""

    model_config = ConfigDict()

    server_host: str = Field(
        default_factory=lambda: os.getenv("RADIUS_SERVER_HOST", "localhost"),
        description="RADIUS server hostname or IP address",
    )
    coa_port: int = Field(
        default_factory=lambda: int(os.getenv("RADIUS_COA_PORT", "3799")),
        description="CoA port (RFC 5176 default: 3799)",
    )
    shared_secret: str = Field(
        default_factory=lambda: os.getenv("RADIUS_SECRET", ""),
        description="RADIUS shared secret",
    )
    dictionary_path: str = Field(
        default_factory=lambda: os.getenv(
            "RADIUS_DICTIONARY_PATH", "/etc/raddb/dictionary"
        ),
        description="Path to RADIUS dictionary file",
    )
    dictionary_coa_path: str | None = Field(
        default_factory=lambda: os.getenv(
            "RADIUS_DICTIONARY_COA_PATH", "/etc/raddb/dictionary.rfc5176"
        ),
        description="Path to CoA dictionary file",
    )
    timeout_seconds: int = Field(
        default_factory=lambda: int(os.getenv("RADIUS_TIMEOUT", "5")),
        description="RADIUS request timeout in seconds",
    )
    max_retries: int = Field(
        default_factory=lambda: int(os.getenv("RADIUS_MAX_RETRIES", "2")),
        description="Maximum retry attempts",
    )
    use_http_api: bool = Field(
        default_factory=lambda: os.getenv("RADIUS_USE_HTTP_API", "false").lower()
        in {"true", "1"},
        description="Use HTTP API instead of native RADIUS protocol",
    )
    http_api_url: str | None = Field(
        default_factory=lambda: os.getenv("RADIUS_HTTP_API_URL"),
        description="HTTP API endpoint URL for CoA operations",
    )
    http_api_key: str = Field(
        default_factory=lambda: os.getenv("RADIUS_HTTP_API_KEY", ""),
        description="HTTP API authentication key",
    )
    default_vendor: str = Field(
        default_factory=lambda: os.getenv("RADIUS_DEFAULT_VENDOR", "mikrotik"),
        description="Default NAS vendor (mikrotik, cisco, huawei, juniper, generic)",
    )
    vendor_aware: bool = Field(
        default_factory=lambda: os.getenv("RADIUS_VENDOR_AWARE", "true").lower()
        in {"true", "1"},
        description="Enable vendor-specific attribute generation",
    )


class FeatureSettings(BaseModel):
    """Feature flags for ISP application."""

    model_config = ConfigDict()

    radius_enabled: bool = Field(
        default_factory=lambda: os.getenv("FEATURE_RADIUS_ENABLED", "true").lower()
        in {"true", "1"},
        description="Enable RADIUS integration",
    )
    voltha_enabled: bool = Field(
        default_factory=lambda: os.getenv("FEATURE_VOLTHA_ENABLED", "true").lower()
        in {"true", "1"},
        description="Enable VOLTHA PON controller integration",
    )
    genieacs_enabled: bool = Field(
        default_factory=lambda: os.getenv("FEATURE_GENIEACS_ENABLED", "true").lower()
        in {"true", "1"},
        description="Enable GenieACS TR-069 integration",
    )
    network_monitoring_enabled: bool = Field(
        default_factory=lambda: os.getenv("FEATURE_NETWORK_MONITORING_ENABLED", "true").lower()
        in {"true", "1"},
        description="Enable network monitoring features",
    )


class OSSSettings(BaseModel):
    """Operational support system integrations."""

    model_config = ConfigDict()

    voltha: ServiceEndpointSettings = Field(
        default_factory=lambda: ServiceEndpointSettings(
            url=os.getenv("VOLTHA_URL", "http://localhost:8881"),
            username=os.getenv("VOLTHA_USERNAME"),
            password=os.getenv("VOLTHA_PASSWORD"),
            api_token=os.getenv("VOLTHA_TOKEN"),
            verify_ssl=os.getenv("VOLTHA_VERIFY_SSL", "true").lower() not in {"false", "0"},
        ),
        description="VOLTHA PON controller configuration",
    )
    genieacs: ServiceEndpointSettings = Field(
        default_factory=lambda: ServiceEndpointSettings(
            url=os.getenv("GENIEACS_URL", "http://localhost:7557"),
            username=os.getenv("GENIEACS_USERNAME"),
            password=os.getenv("GENIEACS_PASSWORD"),
            api_token=os.getenv("GENIEACS_API_TOKEN"),
            verify_ssl=os.getenv("GENIEACS_VERIFY_SSL", "true").lower()
            not in {"false", "0"},
        ),
        description="GenieACS TR-069 controller configuration",
    )
    prometheus: ServiceEndpointSettings = Field(
        default_factory=lambda: ServiceEndpointSettings(
            url=os.getenv("PROMETHEUS_URL", "http://localhost:9090"),
            api_token=os.getenv("PROMETHEUS_API_TOKEN"),
            verify_ssl=os.getenv("PROMETHEUS_VERIFY_SSL", "true").lower()
            not in {"false", "0"},
        ),
        description="Prometheus metrics API configuration",
    )


class TimescaleDBSettings(BaseModel):
    """TimescaleDB configuration for time-series data."""

    model_config = ConfigDict()

    enabled: bool = Field(
        default_factory=lambda: os.getenv("TIMESCALEDB_ENABLED", "false").lower()
        in {"true", "1"},
        description="Enable TimescaleDB for time-series data",
    )
    database_url: str | None = Field(
        default_factory=lambda: os.getenv("TIMESCALEDB_URL"),
        description="TimescaleDB connection URL",
    )

    @property
    def is_configured(self) -> bool:
        """Check if TimescaleDB is configured."""
        return self.enabled and bool(self.database_url)


class Settings(BaseSettings):
    """ISP Application Settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    # Core settings
    environment: Environment = Field(
        default_factory=lambda: Environment(os.getenv("ENVIRONMENT", "development").lower()),
        description="Application environment",
    )
    debug: bool = Field(
        default_factory=lambda: os.getenv("DEBUG", "false").lower() in {"true", "1"},
        description="Enable debug mode",
    )
    testing: bool = Field(
        default_factory=lambda: os.getenv("TESTING", "false").lower() in {"true", "1"},
        description="Enable testing mode",
    )
    secret_key: str = Field(
        default_factory=lambda: os.getenv("SECRET_KEY", "change-me-in-production"),
        description="Application secret key",
    )

    # Database
    database_url: str = Field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/dotmac_isp"
        ),
        description="Database connection URL",
    )
    sync_database_url: str = Field(
        default_factory=lambda: os.getenv(
            "SYNC_DATABASE_URL",
            os.getenv(
                "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/dotmac_isp"
            ).replace("+asyncpg", ""),
        ),
        description="Synchronous database URL for migrations",
    )

    # Redis
    redis_url: str = Field(
        default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        description="Redis connection URL",
    )

    # Service info
    service_name: str = Field(
        default="dotmac-isp",
        description="Service name for observability",
    )
    app_version: str = Field(
        default_factory=lambda: os.getenv("APP_VERSION", "1.0.0"),
        description="Application version",
    )
    tenant_id: str | None = Field(
        default_factory=lambda: os.getenv("TENANT_ID"),
        description="Tenant ID for this ISP instance",
    )

    # Nested settings
    features: FeatureSettings = Field(
        default_factory=FeatureSettings,
        description="Feature flags",
    )
    platform: PlatformConnectionSettings = Field(
        default_factory=PlatformConnectionSettings,
        description="Platform connection settings",
    )
    radius: RADIUSSettings = Field(
        default_factory=RADIUSSettings,
        description="RADIUS configuration",
    )
    oss: OSSSettings = Field(
        default_factory=OSSSettings,
        description="OSS integrations",
    )
    timescaledb: TimescaleDBSettings = Field(
        default_factory=TimescaleDBSettings,
        description="TimescaleDB configuration",
    )

    # Database pool settings
    db_pool_size: int = Field(
        default_factory=lambda: int(os.getenv("DB_POOL_SIZE", "5")),
        description="Database connection pool size",
    )
    db_max_overflow: int = Field(
        default_factory=lambda: int(os.getenv("DB_MAX_OVERFLOW", "10")),
        description="Max connections above pool size",
    )
    db_pool_recycle: int = Field(
        default_factory=lambda: int(os.getenv("DB_POOL_RECYCLE", "3600")),
        description="Seconds before recycling connections",
    )
    db_pool_timeout: int = Field(
        default_factory=lambda: int(os.getenv("DB_POOL_TIMEOUT", "30")),
        description="Seconds to wait for connection",
    )
    db_echo: bool = Field(
        default_factory=lambda: os.getenv("DB_ECHO", "false").lower() in {"true", "1"},
        description="Echo SQL statements",
    )

    # Deployment settings
    deployment_mode: str = Field(
        default_factory=lambda: os.getenv("DEPLOYMENT_MODE", "multi_tenant"),
        description="Deployment mode: single_tenant or multi_tenant",
    )
    default_tenant_id: str | None = Field(
        default_factory=lambda: os.getenv("DEFAULT_TENANT_ID"),
        description="Default tenant ID for single-tenant mode",
    )
    default_tenant_slug: str | None = Field(
        default_factory=lambda: os.getenv("DEFAULT_TENANT_SLUG"),
        description="Default tenant slug for single-tenant mode",
    )

    # CORS settings
    cors_enabled: bool = Field(
        default_factory=lambda: os.getenv("CORS_ENABLED", "true").lower() in {"true", "1"},
        description="Enable CORS",
    )
    cors_origins: list[str] = Field(
        default_factory=lambda: os.getenv("CORS_ORIGINS", "*").split(","),
        description="Allowed CORS origins",
    )
    cors_credentials: bool = Field(
        default_factory=lambda: os.getenv("CORS_CREDENTIALS", "true").lower() in {"true", "1"},
        description="Allow CORS credentials",
    )
    cors_methods: list[str] = Field(
        default_factory=lambda: os.getenv("CORS_METHODS", "GET,POST,PUT,DELETE,PATCH,OPTIONS").split(","),
        description="Allowed CORS methods",
    )
    cors_headers: list[str] = Field(
        default_factory=lambda: os.getenv("CORS_HEADERS", "*").split(","),
        description="Allowed CORS headers",
    )
    cors_max_age: int = Field(
        default_factory=lambda: int(os.getenv("CORS_MAX_AGE", "600")),
        description="CORS preflight cache max age",
    )

    # App version
    app_version: str = Field(
        default_factory=lambda: os.getenv("APP_VERSION", "0.1.0"),
        description="Application version",
    )

    @property
    def async_database_url(self) -> str:
        """Get async database URL (ensure asyncpg driver)."""
        url = self.database_url
        if "+asyncpg" not in url and url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://")
        return url

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == Environment.PRODUCTION

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == Environment.DEVELOPMENT

    @property
    def is_testing(self) -> bool:
        """Check if running in test mode."""
        return self.testing or self.environment == Environment.TEST


# Global settings instance
_settings: Settings | None = None


def get_settings() -> Settings:
    """Get global settings instance (singleton)."""
    global _settings
    if _settings is None:
        _settings = Settings()  # type: ignore
    return _settings


def reset_settings() -> None:
    """Reset settings (mainly for testing)."""
    global _settings
    _settings = None


# Convenience export
settings = get_settings()
