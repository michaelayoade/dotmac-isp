"""
ISP billing adapters.

Implements dotmac.billing interfaces for ISP-specific functionality.
These adapters bridge ISP's subscriber models to the billing system.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dotmac.billing.interfaces import (
    AuditLogger,
    BillingEvent,
    CustomerInfo,
    CustomerProvider,
    EmailContent,
    EmailSender,
    EventPublisher,
    SubscriberInfo,
    SubscriberProvider,
)

if TYPE_CHECKING:
    pass

logger = structlog.get_logger(__name__)


class ISPSubscriberProvider(SubscriberProvider):
    """
    ISP implementation of SubscriberProvider.

    Fetches subscriber data from ISP's subscriber tables.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_subscriber(self, tenant_id: str, subscriber_id: str) -> SubscriberInfo | None:
        """Get subscriber information by ID."""
        try:
            # Import here to avoid circular imports
            from dotmac.isp.subscribers.models import Subscriber

            result = await self.db.execute(
                select(Subscriber).where(
                    Subscriber.tenant_id == tenant_id,
                    Subscriber.id == subscriber_id,
                )
            )
            subscriber = result.scalar_one_or_none()

            if not subscriber:
                return None

            return SubscriberInfo(
                id=str(subscriber.id),
                tenant_id=tenant_id,
                customer_id=str(subscriber.customer_id) if hasattr(subscriber, "customer_id") else str(subscriber.id),
                email=subscriber.email or "",
                name=subscriber.name or f"{subscriber.first_name or ''} {subscriber.last_name or ''}".strip(),
                service_address=subscriber.service_address if hasattr(subscriber, "service_address") else None,
                billing_address=subscriber.billing_address if hasattr(subscriber, "billing_address") else None,
                plan_id=str(subscriber.plan_id) if hasattr(subscriber, "plan_id") and subscriber.plan_id else None,
                status=subscriber.status if hasattr(subscriber, "status") else "active",
                metadata=subscriber.metadata if hasattr(subscriber, "metadata") else None,
            )
        except Exception as e:
            logger.error("Failed to get subscriber", subscriber_id=subscriber_id, error=str(e))
            return None

    async def get_subscriber_by_customer(
        self, tenant_id: str, customer_id: str
    ) -> SubscriberInfo | None:
        """Get subscriber by customer ID."""
        try:
            from dotmac.isp.subscribers.models import Subscriber

            result = await self.db.execute(
                select(Subscriber).where(
                    Subscriber.tenant_id == tenant_id,
                    Subscriber.customer_id == customer_id,
                )
            )
            subscriber = result.scalar_one_or_none()

            if not subscriber:
                return None

            return SubscriberInfo(
                id=str(subscriber.id),
                tenant_id=tenant_id,
                customer_id=str(subscriber.customer_id) if hasattr(subscriber, "customer_id") else str(subscriber.id),
                email=subscriber.email or "",
                name=subscriber.name or f"{subscriber.first_name or ''} {subscriber.last_name or ''}".strip(),
                service_address=subscriber.service_address if hasattr(subscriber, "service_address") else None,
                billing_address=subscriber.billing_address if hasattr(subscriber, "billing_address") else None,
                plan_id=str(subscriber.plan_id) if hasattr(subscriber, "plan_id") and subscriber.plan_id else None,
                status=subscriber.status if hasattr(subscriber, "status") else "active",
                metadata=subscriber.metadata if hasattr(subscriber, "metadata") else None,
            )
        except Exception as e:
            logger.error("Failed to get subscriber by customer", customer_id=customer_id, error=str(e))
            return None

    async def list_subscribers(
        self,
        tenant_id: str,
        offset: int = 0,
        limit: int = 100,
        filters: dict[str, Any] | None = None,
    ) -> list[SubscriberInfo]:
        """List subscribers with pagination."""
        try:
            from dotmac.isp.subscribers.models import Subscriber

            query = select(Subscriber).where(Subscriber.tenant_id == tenant_id)

            # Apply filters
            if filters:
                if "status" in filters:
                    query = query.where(Subscriber.status == filters["status"])
                if "plan_id" in filters:
                    query = query.where(Subscriber.plan_id == filters["plan_id"])
                if "search" in filters:
                    search = f"%{filters['search']}%"
                    query = query.where(
                        (Subscriber.name.ilike(search)) | (Subscriber.email.ilike(search))
                    )

            query = query.offset(offset).limit(limit)
            result = await self.db.execute(query)
            subscribers = result.scalars().all()

            return [
                SubscriberInfo(
                    id=str(s.id),
                    tenant_id=tenant_id,
                    customer_id=str(s.customer_id) if hasattr(s, "customer_id") else str(s.id),
                    email=s.email or "",
                    name=s.name or f"{s.first_name or ''} {s.last_name or ''}".strip(),
                    service_address=s.service_address if hasattr(s, "service_address") else None,
                    billing_address=s.billing_address if hasattr(s, "billing_address") else None,
                    plan_id=str(s.plan_id) if hasattr(s, "plan_id") and s.plan_id else None,
                    status=s.status if hasattr(s, "status") else "active",
                    metadata=s.metadata if hasattr(s, "metadata") else None,
                )
                for s in subscribers
            ]
        except Exception as e:
            logger.error("Failed to list subscribers", tenant_id=tenant_id, error=str(e))
            return []


class ISPCustomerProvider(CustomerProvider):
    """
    ISP implementation of CustomerProvider.

    Maps ISP subscribers to CustomerInfo for billing operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self._subscriber_provider = ISPSubscriberProvider(db)

    async def get_customer(self, tenant_id: str, customer_id: str) -> CustomerInfo | None:
        """Get customer information by ID (maps to subscriber)."""
        subscriber = await self._subscriber_provider.get_subscriber(tenant_id, customer_id)
        if not subscriber:
            return None

        return CustomerInfo(
            id=subscriber.id,
            tenant_id=tenant_id,
            email=subscriber.email,
            name=subscriber.name,
            billing_address=subscriber.billing_address,
            shipping_address=subscriber.service_address,
            metadata=subscriber.metadata,
        )

    async def get_customer_by_email(self, tenant_id: str, email: str) -> CustomerInfo | None:
        """Get customer information by email."""
        try:
            from dotmac.isp.subscribers.models import Subscriber

            result = await self.db.execute(
                select(Subscriber).where(
                    Subscriber.tenant_id == tenant_id,
                    Subscriber.email == email,
                )
            )
            subscriber = result.scalar_one_or_none()

            if not subscriber:
                return None

            return CustomerInfo(
                id=str(subscriber.id),
                tenant_id=tenant_id,
                email=subscriber.email or "",
                name=subscriber.name or f"{subscriber.first_name or ''} {subscriber.last_name or ''}".strip(),
                billing_address=subscriber.billing_address if hasattr(subscriber, "billing_address") else None,
                shipping_address=subscriber.service_address if hasattr(subscriber, "service_address") else None,
                metadata=subscriber.metadata if hasattr(subscriber, "metadata") else None,
            )
        except Exception as e:
            logger.error("Failed to get customer by email", email=email, error=str(e))
            return None

    async def list_customers(
        self,
        tenant_id: str,
        offset: int = 0,
        limit: int = 100,
        filters: dict[str, Any] | None = None,
    ) -> list[CustomerInfo]:
        """List customers with pagination (maps to subscribers)."""
        subscribers = await self._subscriber_provider.list_subscribers(
            tenant_id, offset, limit, filters
        )

        return [
            CustomerInfo(
                id=s.id,
                tenant_id=tenant_id,
                email=s.email,
                name=s.name,
                billing_address=s.billing_address,
                shipping_address=s.service_address,
                metadata=s.metadata,
            )
            for s in subscribers
        ]


class ISPEventPublisher(EventPublisher):
    """
    ISP implementation of EventPublisher.

    Publishes billing events to ISP's event system.
    """

    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    async def publish(self, event: BillingEvent) -> None:
        """Publish a billing event."""
        logger.info(
            "isp.billing.event.published",
            event_type=event.event_type,
            entity_type=event.entity_type,
            entity_id=event.entity_id,
            tenant_id=event.tenant_id,
        )

        # TODO: Integrate with ISP's event system / webhooks
        # Could trigger service suspension for overdue invoices, etc.

    async def publish_batch(self, events: list[BillingEvent]) -> None:
        """Publish multiple billing events."""
        for event in events:
            await self.publish(event)


class ISPEmailSender(EmailSender):
    """
    ISP implementation of EmailSender.

    Sends billing emails via ISP's notification system.
    """

    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    async def send(self, email: EmailContent) -> bool:
        """Send an email. Returns True if successful."""
        logger.info(
            "isp.billing.email.sent",
            to=email.to,
            subject=email.subject,
        )

        try:
            # TODO: Integrate with ISP's notification service
            return True
        except Exception as e:
            logger.error("Failed to send email", error=str(e))
            return False

    async def send_template(
        self,
        template_name: str,
        to: str | list[str],
        context: dict[str, Any],
        tenant_id: str | None = None,
    ) -> bool:
        """Send an email using a template. Returns True if successful."""
        logger.info(
            "isp.billing.email.template_sent",
            template=template_name,
            to=to,
            tenant_id=tenant_id,
        )

        try:
            # TODO: Integrate with ISP's email template service
            return True
        except Exception as e:
            logger.error("Failed to send template email", error=str(e))
            return False


class ISPAuditLogger(AuditLogger):
    """
    ISP implementation of AuditLogger.

    Logs billing audit events to ISP's audit system.
    """

    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    async def log(
        self,
        tenant_id: str,
        action: str,
        entity_type: str,
        entity_id: str,
        user_id: str | None,
        changes: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Log an audit event."""
        logger.info(
            "isp.billing.audit",
            tenant_id=tenant_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            changes=changes,
        )

        # TODO: Integrate with ISP's audit logging


def create_isp_billing_config(db: AsyncSession) -> "BillingServiceConfig":
    """
    Create a BillingServiceConfig with ISP adapters.

    Usage:
        from dotmac.isp.billing_adapters import create_isp_billing_config
        from dotmac.isp.billing.services.invoice import InvoiceService

        config = create_isp_billing_config(db)
        invoice_service = InvoiceService(db, config=config)
    """
    from dotmac.billing.interfaces import BillingServiceConfig

    return BillingServiceConfig(
        customer_provider=ISPCustomerProvider(db),
        subscriber_provider=ISPSubscriberProvider(db),
        event_publisher=ISPEventPublisher(db),
        email_sender=ISPEmailSender(db),
        audit_logger=ISPAuditLogger(db),
    )


__all__ = [
    "ISPSubscriberProvider",
    "ISPCustomerProvider",
    "ISPEventPublisher",
    "ISPEmailSender",
    "ISPAuditLogger",
    "create_isp_billing_config",
]
