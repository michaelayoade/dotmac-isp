"""
Subscriber Management Router.

API endpoints for subscriber CRUD, activation, and status management.
"""

from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from dotmac.shared.auth.dependencies import get_current_user
from dotmac.shared.db import get_async_session
from dotmac.shared.tenant.dependencies import get_current_tenant_id

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
    SubscriberUpdate,
)
from dotmac.isp.subscribers.service import SubscriberService
from dotmac.isp.services.lifecycle.models import ServiceType

logger = structlog.get_logger(__name__)

router = APIRouter()


# =============================================================================
# Dependencies
# =============================================================================


async def get_subscriber_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    tenant_id: Annotated[str, Depends(get_current_tenant_id)],
) -> SubscriberService:
    """Get subscriber service instance."""
    return SubscriberService(session, tenant_id)


# =============================================================================
# CRUD Endpoints
# =============================================================================


@router.post(
    "",
    response_model=SubscriberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create subscriber",
    description="Create a new subscriber with optional RADIUS auto-activation.",
)
async def create_subscriber(
    data: SubscriberCreate,
    service: Annotated[SubscriberService, Depends(get_subscriber_service)],
    _user: Annotated[dict, Depends(get_current_user)],
) -> SubscriberResponse:
    """Create a new subscriber."""
    try:
        return await service.create_subscriber(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "",
    response_model=SubscriberList,
    summary="List subscribers",
    description="List subscribers with filtering and pagination.",
)
async def list_subscribers(
    service: Annotated[SubscriberService, Depends(get_subscriber_service)],
    _user: Annotated[dict, Depends(get_current_user)],
    search: str | None = Query(None, description="Search term"),
    status_filter: SubscriberStatusFilter = Query(
        SubscriberStatusFilter.ALL, alias="status", description="Filter by status"
    ),
    service_type: ServiceType | None = Query(None, description="Filter by service type"),
    customer_id: str | None = Query(None, description="Filter by customer ID"),
    site_id: str | None = Query(None, description="Filter by site ID"),
    nas_identifier: str | None = Query(None, description="Filter by NAS"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_desc: bool = Query(True, description="Sort descending"),
) -> SubscriberList:
    """List subscribers with filters."""
    from uuid import UUID

    query = SubscriberQuery(
        search=search,
        status=status_filter,
        service_type=service_type,
        customer_id=UUID(customer_id) if customer_id else None,
        site_id=site_id,
        nas_identifier=nas_identifier,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )
    return await service.list_subscribers(query)


@router.get(
    "/stats",
    response_model=SubscriberStats,
    summary="Get subscriber statistics",
    description="Get aggregate statistics for subscribers.",
)
async def get_subscriber_stats(
    service: Annotated[SubscriberService, Depends(get_subscriber_service)],
    _user: Annotated[dict, Depends(get_current_user)],
) -> SubscriberStats:
    """Get subscriber statistics."""
    return await service.get_stats()


@router.get(
    "/by-username/{username}",
    response_model=SubscriberResponse,
    summary="Get subscriber by username",
    description="Look up a subscriber by their RADIUS username.",
)
async def get_subscriber_by_username(
    username: str,
    service: Annotated[SubscriberService, Depends(get_subscriber_service)],
    _user: Annotated[dict, Depends(get_current_user)],
) -> SubscriberResponse:
    """Get subscriber by username."""
    subscriber = await service.get_subscriber_by_username(username)
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscriber with username '{username}' not found",
        )
    return subscriber


@router.get(
    "/{subscriber_id}",
    response_model=SubscriberResponse,
    summary="Get subscriber",
    description="Get a subscriber by ID.",
)
async def get_subscriber(
    subscriber_id: str,
    service: Annotated[SubscriberService, Depends(get_subscriber_service)],
    _user: Annotated[dict, Depends(get_current_user)],
) -> SubscriberResponse:
    """Get subscriber by ID."""
    subscriber = await service.get_subscriber(subscriber_id)
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscriber '{subscriber_id}' not found",
        )
    return subscriber


@router.patch(
    "/{subscriber_id}",
    response_model=SubscriberResponse,
    summary="Update subscriber",
    description="Update subscriber fields (partial update).",
)
async def update_subscriber(
    subscriber_id: str,
    data: SubscriberUpdate,
    service: Annotated[SubscriberService, Depends(get_subscriber_service)],
    _user: Annotated[dict, Depends(get_current_user)],
) -> SubscriberResponse:
    """Update subscriber."""
    subscriber = await service.update_subscriber(subscriber_id, data)
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscriber '{subscriber_id}' not found",
        )
    return subscriber


@router.delete(
    "/{subscriber_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete subscriber",
    description="Soft-delete a subscriber (or hard-delete with query param).",
)
async def delete_subscriber(
    subscriber_id: str,
    service: Annotated[SubscriberService, Depends(get_subscriber_service)],
    _user: Annotated[dict, Depends(get_current_user)],
    hard_delete: bool = Query(False, description="Permanently delete"),
) -> None:
    """Delete subscriber."""
    deleted = await service.delete_subscriber(subscriber_id, hard_delete=hard_delete)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscriber '{subscriber_id}' not found",
        )


# =============================================================================
# Lifecycle Endpoints
# =============================================================================


@router.post(
    "/{subscriber_id}/activate",
    response_model=SubscriberActivationResponse,
    summary="Activate subscriber",
    description="Activate a pending subscriber and create RADIUS credentials.",
)
async def activate_subscriber(
    subscriber_id: str,
    data: SubscriberActivate,
    service: Annotated[SubscriberService, Depends(get_subscriber_service)],
    _user: Annotated[dict, Depends(get_current_user)],
) -> SubscriberActivationResponse:
    """Activate subscriber."""
    try:
        result = await service.activate_subscriber(subscriber_id, data)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subscriber '{subscriber_id}' not found",
            )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{subscriber_id}/status",
    response_model=SubscriberResponse,
    summary="Change subscriber status",
    description="Change subscriber status (suspend, terminate, etc.).",
)
async def change_subscriber_status(
    subscriber_id: str,
    data: SubscriberStatusChange,
    service: Annotated[SubscriberService, Depends(get_subscriber_service)],
    _user: Annotated[dict, Depends(get_current_user)],
) -> SubscriberResponse:
    """Change subscriber status."""
    subscriber = await service.change_status(subscriber_id, data)
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscriber '{subscriber_id}' not found",
        )
    return subscriber


@router.post(
    "/{subscriber_id}/suspend",
    response_model=SubscriberResponse,
    summary="Suspend subscriber",
    description="Suspend a subscriber and disconnect active sessions.",
)
async def suspend_subscriber(
    subscriber_id: str,
    service: Annotated[SubscriberService, Depends(get_subscriber_service)],
    _user: Annotated[dict, Depends(get_current_user)],
    reason: str | None = Query(None, description="Reason for suspension"),
) -> SubscriberResponse:
    """Suspend subscriber."""
    subscriber = await service.suspend_subscriber(subscriber_id, reason)
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscriber '{subscriber_id}' not found",
        )
    return subscriber


@router.post(
    "/{subscriber_id}/terminate",
    response_model=SubscriberResponse,
    summary="Terminate subscriber",
    description="Terminate a subscriber permanently.",
)
async def terminate_subscriber(
    subscriber_id: str,
    service: Annotated[SubscriberService, Depends(get_subscriber_service)],
    _user: Annotated[dict, Depends(get_current_user)],
    reason: str | None = Query(None, description="Reason for termination"),
) -> SubscriberResponse:
    """Terminate subscriber."""
    subscriber = await service.terminate_subscriber(subscriber_id, reason)
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscriber '{subscriber_id}' not found",
        )
    return subscriber


# =============================================================================
# Password Management
# =============================================================================


@router.post(
    "/{subscriber_id}/password",
    response_model=SubscriberPasswordResponse,
    summary="Change password",
    description="Change subscriber RADIUS password.",
)
async def change_password(
    subscriber_id: str,
    data: SubscriberPasswordChange,
    service: Annotated[SubscriberService, Depends(get_subscriber_service)],
    _user: Annotated[dict, Depends(get_current_user)],
) -> SubscriberPasswordResponse:
    """Change subscriber password."""
    result = await service.change_password(subscriber_id, data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscriber '{subscriber_id}' not found",
        )
    return result


@router.post(
    "/{subscriber_id}/rotate-password",
    response_model=SubscriberPasswordResponse,
    summary="Rotate password",
    description="Generate and set a new random password.",
)
async def rotate_password(
    subscriber_id: str,
    service: Annotated[SubscriberService, Depends(get_subscriber_service)],
    _user: Annotated[dict, Depends(get_current_user)],
) -> SubscriberPasswordResponse:
    """Rotate subscriber password."""
    result = await service.rotate_password(subscriber_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscriber '{subscriber_id}' not found",
        )
    return result
