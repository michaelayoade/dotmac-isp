"""ISP User Management models - stub.

User management models are available in Shared auth module.
For full user management, Platform package is required.
"""

from typing import Any

import structlog

logger = structlog.get_logger(__name__)


class User:
    """User stub - use dotmac.shared.auth.core.UserInfo for user data."""
    def __init__(self, **kwargs: Any):
        logger.warning("user_management.stub", message="User model requires Platform package")
        for k, v in kwargs.items():
            setattr(self, k, v)


class UserRole:
    """UserRole stub."""
    def __init__(self, **kwargs: Any):
        for k, v in kwargs.items():
            setattr(self, k, v)


class UserPermission:
    """UserPermission stub."""
    def __init__(self, **kwargs: Any):
        for k, v in kwargs.items():
            setattr(self, k, v)


__all__ = [
    "User",
    "UserRole",
    "UserPermission",
]
