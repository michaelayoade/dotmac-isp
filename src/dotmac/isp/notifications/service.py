"""ISP Notifications service - re-exports from __init__."""

from dotmac.isp.notifications import (
    NotificationService,
    list_notification_plugins,
    register_notification_plugin,
)

__all__ = [
    "NotificationService",
    "register_notification_plugin",
    "list_notification_plugins",
]
