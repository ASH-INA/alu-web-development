#!/usr/bin/env python3
""" BasicAuth class
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Basic authentication class"""

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """Extract Base64 part from Authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Decode a Base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Extract user credentials from decoded Base64 string"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        parts = decoded_base64_authorization_header.split(':', 1)
        return parts[0], parts[1]

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """
        Get User instance based on email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            # Search for user by email
            users = User.search({'email': user_email})

            # Check if users is None or empty list
            if users is None:
                return None
            if len(users) == 0:
                return None

            # Get the first user
            user = users[0]

            # Verify password
            if not user.is_valid_password(user_pwd):
                return None

            return user

        except Exception:
            # Catch any exceptions and return None
            return None
