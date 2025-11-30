"""ISP Sales module - stub implementation.

Provides type stubs for sales functionality.
For full implementation, Platform package is required as a runtime dependency.
"""

from enum import Enum
from typing import TYPE_CHECKING, Any

import structlog

logger = structlog.get_logger(__name__)


class OrderStatus(str, Enum):
    """Order status."""
    DRAFT = "draft"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderType(str, Enum):
    """Order type."""
    NEW = "new"
    UPGRADE = "upgrade"
    DOWNGRADE = "downgrade"
    TRANSFER = "transfer"
    CANCELLATION = "cancellation"


class ActivationStatus(str, Enum):
    """Service activation status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


# Stub classes
class Order:
    """Order stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        logger.warning("sales.order_stub", message="Order requires Platform package")
        for k, v in kwargs.items():
            setattr(self, k, v)


class OrderItem:
    """OrderItem stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ServiceActivation:
    """ServiceActivation stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        for k, v in kwargs.items():
            setattr(self, k, v)


class OrderProcessingService:
    """OrderProcessingService stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        logger.warning("sales.service_stub", message="OrderProcessingService requires Platform package")


class ActivationOrchestrator:
    """ActivationOrchestrator stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        logger.warning("sales.orchestrator_stub", message="ActivationOrchestrator requires Platform package")


class ActivationWorkflow:
    """ActivationWorkflow stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        for k, v in kwargs.items():
            setattr(self, k, v)


__all__ = [
    "Order",
    "OrderItem",
    "OrderStatus",
    "OrderType",
    "ServiceActivation",
    "ActivationStatus",
    "ActivationWorkflow",
    "OrderProcessingService",
    "ActivationOrchestrator",
]
