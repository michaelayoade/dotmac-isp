"""ISP Sales service - stub implementations.

Full implementation requires Platform package.
"""

from typing import Any

import structlog

from dotmac.isp.sales import (
    ActivationOrchestrator,
    OrderProcessingService,
)

logger = structlog.get_logger(__name__)


class TemplateMapper:
    """TemplateMapper stub - requires Platform for full implementation."""

    def __init__(self, **kwargs: Any) -> None:
        logger.warning("sales.service_stub", message="TemplateMapper requires Platform package")

    def map_template(self, template: dict[str, Any]) -> dict[str, Any]:
        """Map a template - stub implementation."""
        return template


__all__ = [
    "OrderProcessingService",
    "ActivationOrchestrator",
    "TemplateMapper",
]
