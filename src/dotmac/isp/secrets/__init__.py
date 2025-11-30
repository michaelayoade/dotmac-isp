"""ISP Secrets module - re-exports from dotmac.shared.secrets.

This module provides secrets management for ISP-specific code,
using the shared secrets utilities.
"""

from dotmac.shared.secrets import (
    AsyncVaultClient,
    DataClassification,
    EncryptedField,
    SECRETS_MAPPING,
    SymmetricEncryptionService,
    VaultAuthenticationError,
    VaultClient,
    VaultError,
    get_vault_secret,
    get_vault_secret_async,
    load_secrets_from_vault,
    load_secrets_from_vault_sync,
)

# Import vault_config exports if available
try:
    from dotmac.shared.secrets import (
        VaultConnectionConfig,
        VaultConnectionManager,
        check_vault_health,
        get_async_vault_client,
        get_vault_client,
        get_vault_config,
        get_vault_config_from_env,
        get_vault_config_from_settings,
        get_vault_connection_manager,
    )
    HAS_VAULT_CONFIG = True
except ImportError:
    HAS_VAULT_CONFIG = False

__all__ = [
    # Encryption utilities
    "DataClassification",
    "EncryptedField",
    "SymmetricEncryptionService",
    # Vault client
    "VaultClient",
    "AsyncVaultClient",
    "VaultError",
    "VaultAuthenticationError",
    # Secrets loading
    "load_secrets_from_vault",
    "load_secrets_from_vault_sync",
    "get_vault_secret",
    "get_vault_secret_async",
    "SECRETS_MAPPING",
]

if HAS_VAULT_CONFIG:
    __all__.extend([
        "VaultConnectionConfig",
        "VaultConnectionManager",
        "check_vault_health",
        "get_vault_client",
        "get_async_vault_client",
        "get_vault_config",
        "get_vault_config_from_env",
        "get_vault_config_from_settings",
        "get_vault_connection_manager",
    ])
