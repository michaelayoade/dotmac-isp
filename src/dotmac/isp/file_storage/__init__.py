"""ISP File Storage module - stub implementation.

Provides type stubs for file storage functionality.
For full implementation, Platform package is required as a runtime dependency.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Protocol

import structlog

logger = structlog.get_logger(__name__)


class StorageBackend(str, Enum):
    """Storage backend types."""
    LOCAL = "local"
    MINIO = "minio"
    S3 = "s3"
    MEMORY = "memory"


@dataclass
class FileMetadata:
    """File metadata."""
    filename: str
    content_type: str
    size: int = 0
    bucket: str = ""
    path: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FileInfo:
    """MinIO file info."""
    bucket: str
    object_name: str
    size: int = 0
    content_type: str = "application/octet-stream"
    last_modified: datetime | None = None


class FileStorageService:
    """FileStorageService stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        logger.warning("file_storage.service_stub", message="FileStorageService requires Platform package")

    async def upload(self, *args: Any, **kwargs: Any) -> FileMetadata | None:
        """Upload stub."""
        return None

    async def download(self, *args: Any, **kwargs: Any) -> bytes | None:
        """Download stub."""
        return None

    async def delete(self, *args: Any, **kwargs: Any) -> bool:
        """Delete stub."""
        return False


class LocalFileStorage(FileStorageService):
    """LocalFileStorage stub."""
    pass


class MemoryFileStorage(FileStorageService):
    """MemoryFileStorage stub."""
    pass


class MinIOFileStorage(FileStorageService):
    """MinIOFileStorage stub."""
    pass


class MinIOStorage:
    """MinIOStorage stub - requires Platform for full implementation."""
    def __init__(self, **kwargs: Any):
        logger.warning("file_storage.minio_stub", message="MinIOStorage requires Platform package")


def get_storage(**kwargs: Any) -> MinIOStorage | None:
    """Get storage stub."""
    return None


def reset_storage() -> None:
    """Reset storage stub."""
    pass


def get_storage_service(**kwargs: Any) -> FileStorageService | None:
    """Get storage service stub."""
    return None


def register_storage_plugin(name: str, plugin: type) -> None:
    """Register storage plugin stub."""
    logger.warning("file_storage.plugin_stub", name=name, message="Plugin registration requires Platform package")


def list_storage_plugins() -> list[str]:
    """List storage plugins stub."""
    return []


# Router stubs
file_storage_router = None
storage_router = None


__all__ = [
    # MinIO specific
    "MinIOStorage",
    "FileInfo",
    "get_storage",
    "reset_storage",
    # Service and backends
    "StorageBackend",
    "FileMetadata",
    "FileStorageService",
    "LocalFileStorage",
    "MemoryFileStorage",
    "MinIOFileStorage",
    "get_storage_service",
    "register_storage_plugin",
    "list_storage_plugins",
    # Router
    "file_storage_router",
    "storage_router",
]
