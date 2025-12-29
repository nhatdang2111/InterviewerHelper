"""AES-256 encryption for sensitive data like API keys.

Uses machine-derived key from hardware identifiers for local protection.
"""
import base64
import hashlib
import os
import platform
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# Encrypted values are prefixed with this marker
ENCRYPTED_PREFIX = "enc:v1:"


def _get_machine_id() -> str:
    """Get a stable machine identifier for key derivation.

    Combines multiple identifiers for stability across reboots.
    Falls back gracefully if some identifiers unavailable.
    """
    identifiers = []

    # Machine name
    identifiers.append(platform.node())

    # Platform info
    identifiers.append(platform.platform())

    # Username (adds user-specific binding)
    identifiers.append(os.getenv("USERNAME", os.getenv("USER", "default")))

    # Windows-specific: try to get machine GUID
    if platform.system() == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography"
            )
            machine_guid, _ = winreg.QueryValueEx(key, "MachineGuid")
            identifiers.append(machine_guid)
            winreg.CloseKey(key)
        except Exception:
            pass

    return "|".join(identifiers)


def _derive_key(salt: bytes) -> bytes:
    """Derive encryption key from machine ID using PBKDF2."""
    machine_id = _get_machine_id().encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,  # OWASP recommended minimum
    )

    key = base64.urlsafe_b64encode(kdf.derive(machine_id))
    return key


def _get_or_create_salt() -> bytes:
    """Get or create salt file for key derivation.

    Salt is stored separately from encrypted data for defense in depth.
    """
    salt_dir = Path(__file__).parent.parent / "data"
    salt_dir.mkdir(parents=True, exist_ok=True)
    salt_file = salt_dir / ".salt"

    if salt_file.exists():
        return salt_file.read_bytes()

    # Generate new 16-byte salt
    salt = os.urandom(16)
    salt_file.write_bytes(salt)

    # Set file as hidden on Windows
    if platform.system() == "Windows":
        try:
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(str(salt_file), 0x02)
        except Exception:
            pass

    return salt


def encrypt(plaintext: str) -> str:
    """Encrypt a string value.

    Args:
        plaintext: The value to encrypt

    Returns:
        Encrypted value with prefix marker
    """
    if not plaintext:
        return ""

    # Already encrypted? Return as-is
    if plaintext.startswith(ENCRYPTED_PREFIX):
        return plaintext

    salt = _get_or_create_salt()
    key = _derive_key(salt)
    fernet = Fernet(key)

    encrypted = fernet.encrypt(plaintext.encode())
    return ENCRYPTED_PREFIX + base64.urlsafe_b64encode(encrypted).decode()


class DecryptionError(Exception):
    """Raised when decryption fails due to key change or corruption."""
    pass


def decrypt(ciphertext: str, silent: bool = True) -> str:
    """Decrypt an encrypted string value.

    Args:
        ciphertext: The encrypted value with prefix marker
        silent: If True, return empty string on failure. If False, raise DecryptionError.

    Returns:
        Decrypted plaintext, or original value if not encrypted

    Raises:
        DecryptionError: If silent=False and decryption fails
    """
    if not ciphertext:
        return ""

    # Not encrypted? Return as-is (handles migration)
    if not ciphertext.startswith(ENCRYPTED_PREFIX):
        return ciphertext

    try:
        salt = _get_or_create_salt()
        key = _derive_key(salt)
        fernet = Fernet(key)

        # Remove prefix and decode
        encrypted_b64 = ciphertext[len(ENCRYPTED_PREFIX):]
        encrypted = base64.urlsafe_b64decode(encrypted_b64)

        return fernet.decrypt(encrypted).decode()
    except Exception as e:
        # Decryption failed - key changed or data corrupted
        if silent:
            # Return empty to force re-entry of API key
            return ""
        raise DecryptionError(
            "Failed to decrypt. System configuration may have changed. "
            "Please re-enter your API keys in Settings."
        ) from e


def is_encrypted(value: str) -> bool:
    """Check if a value is encrypted."""
    return value.startswith(ENCRYPTED_PREFIX) if value else False
