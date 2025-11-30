"""
Services Module.

Orchestration and management of ISP services.
"""

from typing import Any

__all__ = ["OrchestrationService"]


def __getattr__(name: str) -> Any:
    """Lazily import heavy submodules to avoid circular imports."""
    if name == "OrchestrationService":
        from dotmac.isp.services.orchestration import OrchestrationService

        return OrchestrationService
    raise AttributeError(f"module 'dotmac.isp.services' has no attribute {name!r}")
