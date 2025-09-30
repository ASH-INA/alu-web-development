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

        # Split on the first colon only to handle passwords with colons
        parts = decoded_base64_authorization_header.split(':', 1)
        if len(parts) != 2:
            return None, None

        return parts[0], parts[1]

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """Get User instance based on email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            # Search for user by email
            users = User.search({'email': user_email})
            if not users or len(users) == 0:
                return None

            user = users[0]
            if not user.is_valid_password(user_pwd):
                return None

            return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get User instance for a request using Basic Authentication"""
        if request is None:
            return None

        # Get authorization header
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Extract Base64 part
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None

        # Decode Base64
        decoded_base64 = self.decode_base64_authorization_header(base64_auth)
        if decoded_base64 is None:
            return None

        # Extract user credentials
        user_email, user_pwd = self.extract_user_credentials(decoded_base64)
        if user_email is None or user_pwd is None:
            return None

        # Get user object from credentials
        return self.user_object_from_credentials(user_email, user_pwd)
