#!/usr/bin/env python3
""" BasicAuth class
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic authentication class"""

    # def extract_base64_authorization_header(self, authorization_header: str) -> str:
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """Extract the Base64 part from the Authorization header

        Args:
            authorization_header: The Authorization header string

        Returns:
            The Base64 encoded string after 'Basic ' prefix, or None if invalid
        """
        # Return None if authorization_header is None
        if authorization_header is None:
            return None

        # Return None if authorization_header is not a string
        if not isinstance(authorization_header, str):
            return None

        # Return None if authorization_header doesn't start with 'Basic '
        if not authorization_header.startswith('Basic '):
            return None

        # Return the value after 'Basic ' (after the space)
        return authorization_header[6:]
