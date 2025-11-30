"""ISP CRM module - stub implementation.

Provides type stubs for CRM functionality.
For full implementation, Platform package is required as a runtime dependency.
"""

from enum import Enum
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


class LeadStatus(str, Enum):
    """Lead status."""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    LOST = "lost"


class LeadSource(str, Enum):
    """Lead source."""
    WEBSITE = "website"
    REFERRAL = "referral"
    MARKETING = "marketing"
    DIRECT = "direct"
    OTHER = "other"


class QuoteStatus(str, Enum):
    """Quote status."""
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class SiteSurveyStatus(str, Enum):
    """Site survey status."""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Stub classes
class Lead:
    """Lead stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Quote:
    """Quote stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        for k, v in kwargs.items():
            setattr(self, k, v)


class SiteSurvey:
    """SiteSurvey stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Serviceability:
    """Serviceability stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        for k, v in kwargs.items():
            setattr(self, k, v)


class LeadService:
    """LeadService stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        logger.warning("crm.service_stub", message="LeadService requires Platform package")


class QuoteService:
    """QuoteService stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        logger.warning("crm.service_stub", message="QuoteService requires Platform package")


class SiteSurveyService:
    """SiteSurveyService stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        logger.warning("crm.service_stub", message="SiteSurveyService requires Platform package")


__all__ = [
    # Models
    "Lead",
    "LeadStatus",
    "LeadSource",
    "Quote",
    "QuoteStatus",
    "SiteSurvey",
    "SiteSurveyStatus",
    "Serviceability",
    # Services
    "LeadService",
    "QuoteService",
    "SiteSurveyService",
]
