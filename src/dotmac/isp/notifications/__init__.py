"""ISP Notifications module.

Re-exports shared notification types and interfaces.
For full notification service implementations, Platform package is required.
"""

from dotmac.shared.notifications import (
    NotificationChannel,
    NotificationDTO,
    NotificationPriority,
    NotificationServiceProtocol,
    NotificationType,
)

# Backward compatibility aliases
Notification = NotificationDTO
NotificationPreference = None  # Not available in shared - requires Platform
NotificationTemplate = None  # Not available in shared - requires Platform
NotificationService = None  # Not available in shared - requires Platform


def register_notification_plugin(name: str, plugin: type) -> None:
    """Stub for plugin registration - requires Platform for full functionality."""
    import structlog
    logger = structlog.get_logger(__name__)
    logger.warning(
        "notifications.plugin_registration_stub",
        name=name,
        message="Plugin registration requires Platform package for full functionality",
    )


def list_notification_plugins() -> list[str]:
    """Stub for listing plugins - requires Platform for full functionality."""
    return []


__all__ = [
    # Types from Shared
    "NotificationType",
    "NotificationPriority",
    "NotificationChannel",
    "NotificationDTO",
    "NotificationServiceProtocol",
    # Backward compatibility aliases
    "Notification",
    "NotificationPreference",
    "NotificationTemplate",
    "NotificationService",
    # Plugin stubs
    "register_notification_plugin",
    "list_notification_plugins",
]
