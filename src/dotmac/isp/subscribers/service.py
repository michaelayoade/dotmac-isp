"""
Subscriber Service Layer.

Business logic for subscriber management operations.
Integrates with RADIUS for authentication and billing for subscriptions.
"""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

import structlog
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from dotmac.isp.subscribers.models import (
    PasswordHashingMethod,
    Subscriber,
    SubscriberStatus,
    generate_random_password,
    hash_radius_password,
)
from dotmac.isp.subscribers.schemas import (
    SubscriberActivate,
    SubscriberActivationResponse,
    SubscriberCreate,
    SubscriberList,
    SubscriberPasswordChange,
    SubscriberPasswordResponse,
    SubscriberQuery,
    SubscriberResponse,
    SubscriberStats,
    SubscriberStatusChange,
    SubscriberStatusFilter,
    SubscriberSummary,
    SubscriberUpdate,
)
from dotmac.isp.radius.schemas import RADIUSSubscriberCreate
from dotmac.isp.radius.service import RADIUSService
from dotmac.isp.services.lifecycle.models import ServiceType

logger = structlog.get_logger(__name__)


class SubscriberService:
    """
    Service for subscriber management operations.

    Handles:
    - CRUD operations for subscribers
    - RADIUS credential management
    - Status lifecycle (activate, suspend, terminate)
    - Password management
    - Usage statistics
    """

    def __init__(self, session: AsyncSession, tenant_id: str):
        self.session = session
        self.tenant_id = tenant_id
        self._radius_service: RADIUSService | None = None

    @property
    def radius_service(self) -> RADIUSService:
        """Lazy-load RADIUS service."""
        if self._radius_service is None:
            self._radius_service = RADIUSService(self.session, self.tenant_id)
        return self._radius_service

    # =========================================================================
    # CRUD Operations
    # =========================================================================

    async def create_subscriber(self, data: SubscriberCreate) -> SubscriberResponse:
        """
        Create a new subscriber.

        Args:
            data: Subscriber creation data

        Returns:
            Created subscriber response

        Raises:
            ValueError: If username already exists
        """
        # Check username uniqueness
        existing = await self._get_by_username(data.username)
        if existing:
            raise ValueError(f"Subscriber with username '{data.username}' already exists")

        # Generate password if not provided
        plain_password = data.password or generate_random_password()
        hashed_password = hash_radius_password(plain_password, data.password_hash_method)

        # Create subscriber record
        subscriber = Subscriber(
            id=str(uuid4()),
            tenant_id=self.tenant_id,
            username=data.username,
            password=hashed_password,
            password_hash_method=data.password_hash_method.value,
            subscriber_number=data.subscriber_number,
            full_name=data.full_name,
            email=data.email,
            phone_number=data.phone_number,
            customer_id=data.customer_id,
            user_id=data.user_id,
            status=data.status,
            service_type=data.service_type,
            # Network config
            bandwidth_profile_id=data.network.bandwidth_profile_id,
            download_speed_kbps=data.network.download_speed_kbps,
            upload_speed_kbps=data.network.upload_speed_kbps,
            static_ipv4=data.network.static_ipv4,
            ipv6_prefix=data.network.ipv6_prefix,
            vlan_id=data.network.vlan_id,
            nas_identifier=data.network.nas_identifier,
            # Device config
            onu_serial=data.device.onu_serial,
            cpe_mac_address=data.device.cpe_mac_address,
            device_metadata=data.device.device_metadata,
            # Location config
            service_address=data.location.service_address,
            service_coordinates=data.location.service_coordinates,
            site_id=data.location.site_id,
            # Session config
            session_timeout=data.session.session_timeout,
            idle_timeout=data.session.idle_timeout,
            simultaneous_use=data.session.simultaneous_use,
            # Meta
            metadata_=data.metadata_ or {},
            notes=data.notes,
        )

        self.session.add(subscriber)
        await self.session.flush()

        logger.info(
            "subscriber.created",
            subscriber_id=subscriber.id,
            username=subscriber.username,
            status=subscriber.status.value,
        )

        # Auto-activate if requested
        if data.auto_activate:
            await self._activate_subscriber(subscriber, plain_password)

        await self.session.refresh(subscriber)
        return SubscriberResponse.model_validate(subscriber)

    async def get_subscriber(self, subscriber_id: str) -> SubscriberResponse | None:
        """Get subscriber by ID."""
        subscriber = await self._get_by_id(subscriber_id)
        if not subscriber:
            return None
        return SubscriberResponse.model_validate(subscriber)

    async def get_subscriber_by_username(self, username: str) -> SubscriberResponse | None:
        """Get subscriber by username."""
        subscriber = await self._get_by_username(username)
        if not subscriber:
            return None
        return SubscriberResponse.model_validate(subscriber)

    async def list_subscribers(self, query: SubscriberQuery) -> SubscriberList:
        """
        List subscribers with filtering and pagination.

        Args:
            query: Query parameters

        Returns:
            Paginated list of subscribers
        """
        # Build base query
        stmt = select(Subscriber).where(
            and_(
                Subscriber.tenant_id == self.tenant_id,
                Subscriber.deleted_at.is_(None),
            )
        )

        # Apply filters
        if query.search:
            search_term = f"%{query.search}%"
            stmt = stmt.where(
                or_(
                    Subscriber.username.ilike(search_term),
                    Subscriber.subscriber_number.ilike(search_term),
                    Subscriber.full_name.ilike(search_term),
                    Subscriber.email.ilike(search_term),
                )
            )

        if query.status != SubscriberStatusFilter.ALL:
            stmt = stmt.where(Subscriber.status == query.status.value)

        if query.service_type:
            stmt = stmt.where(Subscriber.service_type == query.service_type)

        if query.customer_id:
            stmt = stmt.where(Subscriber.customer_id == query.customer_id)

        if query.site_id:
            stmt = stmt.where(Subscriber.site_id == query.site_id)

        if query.nas_identifier:
            stmt = stmt.where(Subscriber.nas_identifier == query.nas_identifier)

        if query.created_after:
            stmt = stmt.where(Subscriber.created_at >= query.created_after)

        if query.created_before:
            stmt = stmt.where(Subscriber.created_at <= query.created_before)

        if query.last_online_after:
            stmt = stmt.where(Subscriber.last_online >= query.last_online_after)

        # Count total
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.session.execute(count_stmt)).scalar() or 0

        # Apply sorting
        sort_column = getattr(Subscriber, query.sort_by, Subscriber.created_at)
        if query.sort_desc:
            stmt = stmt.order_by(sort_column.desc())
        else:
            stmt = stmt.order_by(sort_column.asc())

        # Apply pagination
        offset = (query.page - 1) * query.page_size
        stmt = stmt.offset(offset).limit(query.page_size)

        # Execute query
        result = await self.session.execute(stmt)
        subscribers = result.scalars().all()

        # Calculate pages
        pages = (total + query.page_size - 1) // query.page_size

        return SubscriberList(
            items=[SubscriberSummary.model_validate(s) for s in subscribers],
            total=total,
            page=query.page,
            page_size=query.page_size,
            pages=pages,
        )

    async def update_subscriber(
        self, subscriber_id: str, data: SubscriberUpdate
    ) -> SubscriberResponse | None:
        """
        Update an existing subscriber.

        Args:
            subscriber_id: Subscriber ID
            data: Update data (partial updates supported)

        Returns:
            Updated subscriber or None if not found
        """
        subscriber = await self._get_by_id(subscriber_id)
        if not subscriber:
            return None

        # Apply updates (only non-None values)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)

        for field, value in update_data.items():
            if hasattr(subscriber, field):
                setattr(subscriber, field, value)

        await self.session.flush()
        await self.session.refresh(subscriber)

        logger.info(
            "subscriber.updated",
            subscriber_id=subscriber_id,
            fields=list(update_data.keys()),
        )

        return SubscriberResponse.model_validate(subscriber)

    async def delete_subscriber(self, subscriber_id: str, hard_delete: bool = False) -> bool:
        """
        Delete a subscriber.

        Args:
            subscriber_id: Subscriber ID
            hard_delete: If True, permanently delete. If False, soft delete.

        Returns:
            True if deleted, False if not found
        """
        subscriber = await self._get_by_id(subscriber_id)
        if not subscriber:
            return False

        if hard_delete:
            await self.session.delete(subscriber)
        else:
            subscriber.deleted_at = datetime.now(UTC)

        # Clean up RADIUS credentials
        try:
            await self.radius_service.delete_subscriber(subscriber_id)
        except Exception as e:
            logger.warning(
                "subscriber.radius_delete_failed",
                subscriber_id=subscriber_id,
                error=str(e),
            )

        await self.session.flush()

        logger.info(
            "subscriber.deleted",
            subscriber_id=subscriber_id,
            hard_delete=hard_delete,
        )

        return True

    # =========================================================================
    # Status Lifecycle
    # =========================================================================

    async def activate_subscriber(
        self, subscriber_id: str, data: SubscriberActivate
    ) -> SubscriberActivationResponse | None:
        """
        Activate a pending subscriber.

        Creates RADIUS credentials and sets status to active.

        Args:
            subscriber_id: Subscriber ID
            data: Activation options

        Returns:
            Activation response or None if not found
        """
        subscriber = await self._get_by_id(subscriber_id)
        if not subscriber:
            return None

        if subscriber.status not in (SubscriberStatus.PENDING, SubscriberStatus.SUSPENDED):
            raise ValueError(
                f"Cannot activate subscriber with status '{subscriber.status.value}'"
            )

        generated_password: str | None = None

        if data.create_radius_credentials:
            # Generate new password for RADIUS
            generated_password = await self._activate_subscriber(subscriber)

        # Update status
        subscriber.status = SubscriberStatus.ACTIVE
        subscriber.activation_date = datetime.now(UTC)
        subscriber.suspension_date = None

        await self.session.flush()
        await self.session.refresh(subscriber)

        logger.info(
            "subscriber.activated",
            subscriber_id=subscriber_id,
            username=subscriber.username,
        )

        return SubscriberActivationResponse(
            subscriber_id=subscriber.id,
            username=subscriber.username,
            status=subscriber.status,
            radius_credentials_created=data.create_radius_credentials,
            password=generated_password,
            activation_date=subscriber.activation_date,
        )

    async def change_status(
        self, subscriber_id: str, data: SubscriberStatusChange
    ) -> SubscriberResponse | None:
        """
        Change subscriber status.

        Args:
            subscriber_id: Subscriber ID
            data: Status change data

        Returns:
            Updated subscriber or None if not found
        """
        subscriber = await self._get_by_id(subscriber_id)
        if not subscriber:
            return None

        old_status = subscriber.status
        new_status = data.status

        # Update status
        subscriber.status = new_status

        # Set appropriate date
        now = datetime.now(UTC)
        if new_status == SubscriberStatus.ACTIVE:
            if not subscriber.activation_date:
                subscriber.activation_date = now
            subscriber.suspension_date = None
        elif new_status == SubscriberStatus.SUSPENDED:
            subscriber.suspension_date = now
        elif new_status == SubscriberStatus.TERMINATED:
            subscriber.termination_date = now

        # Disconnect active sessions if suspending/terminating
        if data.disconnect_active_sessions and new_status in (
            SubscriberStatus.SUSPENDED,
            SubscriberStatus.TERMINATED,
            SubscriberStatus.DISCONNECTED,
        ):
            try:
                await self.radius_service.disconnect_subscriber_sessions(subscriber.username)
            except Exception as e:
                logger.warning(
                    "subscriber.session_disconnect_failed",
                    subscriber_id=subscriber_id,
                    error=str(e),
                )

        await self.session.flush()
        await self.session.refresh(subscriber)

        logger.info(
            "subscriber.status_changed",
            subscriber_id=subscriber_id,
            old_status=old_status.value,
            new_status=new_status.value,
            reason=data.reason,
        )

        return SubscriberResponse.model_validate(subscriber)

    async def suspend_subscriber(
        self, subscriber_id: str, reason: str | None = None
    ) -> SubscriberResponse | None:
        """Convenience method to suspend a subscriber."""
        return await self.change_status(
            subscriber_id,
            SubscriberStatusChange(
                status=SubscriberStatus.SUSPENDED,
                reason=reason,
                disconnect_active_sessions=True,
            ),
        )

    async def terminate_subscriber(
        self, subscriber_id: str, reason: str | None = None
    ) -> SubscriberResponse | None:
        """Convenience method to terminate a subscriber."""
        return await self.change_status(
            subscriber_id,
            SubscriberStatusChange(
                status=SubscriberStatus.TERMINATED,
                reason=reason,
                disconnect_active_sessions=True,
            ),
        )

    # =========================================================================
    # Password Management
    # =========================================================================

    async def change_password(
        self, subscriber_id: str, data: SubscriberPasswordChange
    ) -> SubscriberPasswordResponse | None:
        """
        Change subscriber password.

        Args:
            subscriber_id: Subscriber ID
            data: Password change data

        Returns:
            Password response with new password or None if not found
        """
        subscriber = await self._get_by_id(subscriber_id)
        if not subscriber:
            return None

        # Generate or use provided password
        plain_password = data.new_password or generate_random_password()
        hashed_password = hash_radius_password(plain_password, data.hash_method)

        # Update subscriber password
        subscriber.password = hashed_password
        subscriber.password_hash_method = data.hash_method.value

        # Update RADIUS credentials if requested
        radius_updated = False
        if data.update_radius:
            try:
                await self.radius_service.update_subscriber_password(
                    subscriber.username, plain_password
                )
                radius_updated = True
            except Exception as e:
                logger.warning(
                    "subscriber.radius_password_update_failed",
                    subscriber_id=subscriber_id,
                    error=str(e),
                )

        await self.session.flush()

        logger.info(
            "subscriber.password_changed",
            subscriber_id=subscriber_id,
            username=subscriber.username,
            radius_updated=radius_updated,
        )

        return SubscriberPasswordResponse(
            subscriber_id=subscriber.id,
            username=subscriber.username,
            new_password=plain_password,
            hash_method=data.hash_method.value,
            radius_updated=radius_updated,
        )

    async def rotate_password(self, subscriber_id: str) -> SubscriberPasswordResponse | None:
        """Generate and set a new random password for a subscriber."""
        return await self.change_password(
            subscriber_id,
            SubscriberPasswordChange(
                new_password=None,  # Auto-generate
                hash_method=PasswordHashingMethod.SHA256,
                update_radius=True,
            ),
        )

    # =========================================================================
    # Statistics
    # =========================================================================

    async def get_stats(self) -> SubscriberStats:
        """Get subscriber statistics for the tenant."""
        base_filter = and_(
            Subscriber.tenant_id == self.tenant_id,
            Subscriber.deleted_at.is_(None),
        )

        # Total count
        total_stmt = select(func.count()).where(base_filter)
        total = (await self.session.execute(total_stmt)).scalar() or 0

        # Status counts
        status_counts = {}
        for status in SubscriberStatus:
            stmt = select(func.count()).where(
                and_(base_filter, Subscriber.status == status)
            )
            status_counts[status.value] = (await self.session.execute(stmt)).scalar() or 0

        # Service type counts
        service_type_stmt = (
            select(Subscriber.service_type, func.count())
            .where(base_filter)
            .group_by(Subscriber.service_type)
        )
        service_type_result = await self.session.execute(service_type_stmt)
        by_service_type = {
            str(st.value): count for st, count in service_type_result.all()
        }

        # Recent activity
        now = datetime.now(UTC)
        from datetime import timedelta

        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)

        new_7_stmt = select(func.count()).where(
            and_(base_filter, Subscriber.created_at >= week_ago)
        )
        new_7 = (await self.session.execute(new_7_stmt)).scalar() or 0

        new_30_stmt = select(func.count()).where(
            and_(base_filter, Subscriber.created_at >= month_ago)
        )
        new_30 = (await self.session.execute(new_30_stmt)).scalar() or 0

        # Online now (last 5 minutes)
        five_min_ago = now - timedelta(minutes=5)
        online_stmt = select(func.count()).where(
            and_(base_filter, Subscriber.last_online >= five_min_ago)
        )
        online_now = (await self.session.execute(online_stmt)).scalar() or 0

        return SubscriberStats(
            total=total,
            active=status_counts.get("active", 0),
            pending=status_counts.get("pending", 0),
            suspended=status_counts.get("suspended", 0),
            terminated=status_counts.get("terminated", 0),
            by_service_type=by_service_type,
            new_last_7_days=new_7,
            new_last_30_days=new_30,
            online_now=online_now,
        )

    # =========================================================================
    # Internal Helpers
    # =========================================================================

    async def _get_by_id(self, subscriber_id: str) -> Subscriber | None:
        """Get subscriber by ID (internal use)."""
        stmt = select(Subscriber).where(
            and_(
                Subscriber.id == subscriber_id,
                Subscriber.tenant_id == self.tenant_id,
                Subscriber.deleted_at.is_(None),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_by_username(self, username: str) -> Subscriber | None:
        """Get subscriber by username (internal use)."""
        stmt = select(Subscriber).where(
            and_(
                Subscriber.username == username,
                Subscriber.tenant_id == self.tenant_id,
                Subscriber.deleted_at.is_(None),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def _activate_subscriber(
        self, subscriber: Subscriber, plain_password: str | None = None
    ) -> str:
        """
        Activate subscriber and create RADIUS credentials.

        Returns the plain password (generated if not provided).
        """
        # Generate password if needed
        if not plain_password:
            plain_password = generate_random_password()
            subscriber.password = hash_radius_password(
                plain_password, PasswordHashingMethod.SHA256
            )
            subscriber.password_hash_method = PasswordHashingMethod.SHA256.value

        # Create RADIUS credentials
        try:
            radius_data = RADIUSSubscriberCreate(
                subscriber_id=subscriber.id,
                username=subscriber.username,
                password=plain_password,
                bandwidth_profile_id=subscriber.bandwidth_profile_id,
                download_kbps=subscriber.download_speed_kbps,
                upload_kbps=subscriber.upload_speed_kbps,
                framed_ipv4_address=subscriber.static_ipv4,
                framed_ipv6_prefix=subscriber.ipv6_prefix,
                session_timeout=subscriber.session_timeout,
                idle_timeout=subscriber.idle_timeout,
                simultaneous_use=subscriber.simultaneous_use,
            )
            await self.radius_service.create_subscriber(radius_data)
        except Exception as e:
            logger.error(
                "subscriber.radius_creation_failed",
                subscriber_id=subscriber.id,
                error=str(e),
            )
            raise

        # Update status
        subscriber.status = SubscriberStatus.ACTIVE
        subscriber.activation_date = datetime.now(UTC)

        return plain_password
