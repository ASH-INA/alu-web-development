#!/usr/bin/env python3
""" BasicAuth class
"""
from api.v1.auth.auth import Auth
import base64


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
        """Extract user credentials from decoded Base64 string

        Args:
            decoded_base64_authorization_header: Decoded Base64 string

        Returns:
            Tuple of (user_email, user_password) or (None, None) if invalid
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split on the first colon only (in case password contains colons)
        user_email, passwor = decoded_base64_authorization_header.split(':', 1)
        return user_email, passwor
