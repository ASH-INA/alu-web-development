#!/usr/bin/env python3
""" BasicAuth class
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Basic authentication class"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extract Base64 part from Authorization header

        Args:
            authorization_header: The Authorization header string

        Returns:
            The Base64 encoded string after 'Basic ' prefix, or None if invalid
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decode a Base64 string

        Args:
            base64_authorization_header: Base64 encoded string

        Returns:
            Decoded UTF-8 string, or None if invalid
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode the Base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            # Convert bytes to UTF-8 string
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None
