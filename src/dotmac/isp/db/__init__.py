"""
ISP Database module - re-exports from dotmac.shared.db.

This module provides backwards compatibility for ISP-specific models
that import from dotmac.isp.db.
"""

from dotmac.shared.db import (
    AuditMixin,
    Base,
    BaseModel,
    SoftDeleteMixin,
    StrictTenantMixin,
    TenantMixin,
    TimestampMixin,
    async_session_maker,
    configure_database,
    configure_database_for_testing,
    create_all_tables,
    get_async_engine,
    get_async_session,
    get_db,
    get_session,
    get_session_dependency,
    get_sync_engine,
)

# Alias for backwards compatibility
get_async_session_contextmanager = get_async_session

__all__ = [
    "AuditMixin",
    "Base",
    "BaseModel",
    "SoftDeleteMixin",
    "StrictTenantMixin",
    "TenantMixin",
    "TimestampMixin",
    "async_session_maker",
    "configure_database",
    "configure_database_for_testing",
    "create_all_tables",
    "get_async_engine",
    "get_async_session",
    "get_async_session_contextmanager",
    "get_db",
    "get_session",
    "get_session_dependency",
    "get_sync_engine",
]
