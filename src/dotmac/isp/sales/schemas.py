"""ISP Sales schemas - stub implementations.

Full implementation requires Platform package.
"""

from typing import Any

import structlog
from pydantic import BaseModel, Field

from dotmac.isp.sales import (
    ActivationStatus,
    OrderStatus,
    OrderType,
)

logger = structlog.get_logger(__name__)


class OrderCreate(BaseModel):
    """Order creation schema - stub implementation."""

    customer_id: str = Field(description="Customer ID")
    order_type: OrderType = Field(default=OrderType.NEW, description="Order type")
    items: list[dict[str, Any]] = Field(default_factory=list, description="Order items")
    notes: str | None = Field(None, description="Order notes")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class OrderSubmit(BaseModel):
    """Order submission schema - stub implementation."""

    order_id: str = Field(description="Order ID to submit")
    payment_method_id: str | None = Field(None, description="Payment method ID")
    notes: str | None = Field(None, description="Submission notes")


class ServiceSelection(BaseModel):
    """Service selection schema - stub implementation."""

    product_id: str = Field(description="Product ID")
    plan_id: str | None = Field(None, description="Plan ID")
    quantity: int = Field(default=1, description="Quantity")
    addons: list[str] = Field(default_factory=list, description="Addon IDs")


class QuickOrderRequest(BaseModel):
    """Quick order request schema - stub implementation."""

    customer_id: str = Field(description="Customer ID")
    services: list[ServiceSelection] = Field(default_factory=list, description="Services to order")
    notes: str | None = Field(None, description="Order notes")


__all__ = [
    "OrderStatus",
    "OrderType",
    "ActivationStatus",
    "OrderCreate",
    "OrderSubmit",
    "ServiceSelection",
    "QuickOrderRequest",
]
