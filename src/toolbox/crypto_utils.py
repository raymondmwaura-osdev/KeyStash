"""
crypto_utils.py

This module provides cryptographic utilities for secure data handling.
It implements password-based key derivation and symmetric encryption
using the Python `cryptography` library.

Functions:
    generate_key(master_password: bytes, salt: bytes) -> bytes
        Derives a Fernet-compatible key from a master password and salt.

    encrypt(contents: bytes, master_password: str | bytes) -> tuple[bytes, bytes]
        Encrypts data using a key derived from a master password and returns
        both the salt and the encrypted ciphertext.

    decrypt(encrypted_contents: bytes, master_password: str | bytes, salt: bytes) -> bytes
        Decrypts ciphertext using the provided master password and salt and
        returns the data.
"""

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import pathlib, base64, os

# NOTE: The functions are arranged alphabetically.

def decrypt(encrypted_contents: bytes, master_password: bytes, salt: bytes) -> bytes:
    """
    Decrypt data using a key derived from a master password and salt.

    This function reverses the encryption performed by `encrypt()` by
    regenerating the same Fernet key and decrypting the ciphertext.

    Parameters:
        encrypted_contents (bytes): The ciphertext to decrypt.
        master_password (bytes): The master password used for encryption.
        salt (bytes): The salt originally used for key derivation.

    Returns:
        bytes: The decrypted plaintext data.
    """
    key = generate_key(master_password, salt)
    return Fernet(key).decrypt(encrypted_contents)

def encrypt(contents: bytes, master_password: bytes) -> tuple[bytes, bytes]:
    """
    Encrypt data using a key derived from a master password.

    The function generates a random salt, derives a Fernet-compatible key
    from the salt and provided password, and encrypts the given data.
    The salt is returned alongside the ciphertext.

    Parameters:
        contents (bytes): The plaintext data to encrypt.
        master_password (bytes): The master password used for key derivation.

    Returns:
        tuple[bytes, bytes]: A tuple containing the salt and the encrypted data `(salt, encrypted_data)`.
    """
    # Generate key.
    salt = os.urandom(16)
    key = generate_key(master_password, salt)

    # Encrypt contents.
    encrypted_contents = Fernet(key).encrypt(contents)

    return salt, encrypted_contents

def generate_key(master_password: bytes, salt: bytes) -> bytes:
    """
    Derive a cryptographic key from a master password and salt.

    This function uses the PBKDF2-HMAC key derivation function with SHA-256
    to derive a 32-byte key from the given password and salt, making it
    suitable for use with the Fernet symmetric encryption system.

    Parameters:
        master_password (bytes): The master password in bytes.
        salt (bytes): A cryptographically secure random salt.

    Returns:
        bytes: A URL-safe, Base64-encoded key for use with Fernet.
    """
    key = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    ).derive(master_password)

    # Make safe for use with Fernet.
    key = base64.urlsafe_b64encode(key)

    return key
