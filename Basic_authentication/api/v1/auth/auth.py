#!/usr/bin/env python3
""" Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Template for all authentication systems"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine if authentication is required

        Args:
            path: The path to check
            excluded_paths: List of paths that don't require authentication
            
        Returns:
            False for now (will be implemented later)
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Get the authorization header from the request

        Args:
            request: The Flask request object

        Returns:
            None for now (will be implemented later)
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request

        Args:
            request: The Flask request object

        Returns:
            None for now (will be implemented later)
        """
        return None
