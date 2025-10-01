#!/usr/bin/env python3
""" Authentication module for user authentication service
"""
import bcrypt


def _hash_password(password: str) -> str:
    """Hash a password using bcrypt

    Args:
        password: The password string to hash

    Returns:
        A salted hash of the password as a string
    """
    # Convert password to bytes
    password_bytes = password.encode('utf-8')

    # Generate salt and hash the password
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # Return the hashed password as string
    return hashed.decode('utf-8')
