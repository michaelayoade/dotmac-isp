"""ISP Auth Module - imports from shared auth."""

from dotmac.shared.auth import (
    # Services
    APIKeyService,
    JWTService,
    SessionManager,
    api_key_service,
    jwt_service,
    session_manager,
    # Models
    TokenData,
    TokenType,
    UserInfo,
    # Dependencies
    get_current_user,
    get_current_user_optional,
    require_admin,
    require_auth,
    require_roles,
    require_scopes,
    security,
    # Utils
    configure_auth,
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    # Exceptions
    AuthenticationError,
    AuthError,
    InvalidToken,
    TokenExpired,
    get_http_status,
)

__all__ = [
    # Services
    "JWTService",
    "SessionManager",
    "APIKeyService",
    "jwt_service",
    "session_manager",
    "api_key_service",
    # Models
    "UserInfo",
    "TokenData",
    "TokenType",
    # Dependencies
    "get_current_user",
    "get_current_user_optional",
    "require_auth",
    "require_admin",
    "require_scopes",
    "require_roles",
    "security",
    # Utils
    "hash_password",
    "verify_password",
    "create_access_token",
    "create_refresh_token",
    "configure_auth",
    # Exceptions
    "AuthError",
    "AuthenticationError",
    "TokenExpired",
    "InvalidToken",
    "get_http_status",
]
