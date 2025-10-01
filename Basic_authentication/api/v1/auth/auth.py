#!/usr/bin/env python3
""" Auth class
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Template for all authentication systems"""

    def require_auth(
        self, path: str, excluded_paths: List[str]
    ) -> bool:
        """Determine if authentication is required

        Args:
            path: The path to check
            excluded_paths: List of paths that don't require authentication

        Returns:
            True if authentication is required, False otherwise
        """
        # If path is None, return True (requires auth)
        if path is None:
            return True

        # If excluded_paths is None or empty, return True (requires auth)
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure path ends with a slash for consistent comparison
        if not path.endswith('/'):
            path += '/'

        # Check if path is in excluded_paths or matches wildcard pattern
        for excluded_path in excluded_paths:
            # Ensure excluded_path ends with slash for comparison
            if not excluded_path.endswith('/'):
                excluded_path += '/'

            # Check for exact match
            if path == excluded_path:
                return False

            # Check for wildcard match
            if excluded_path.endswith('*/'):
                # Remove the wildcard and compare prefix
                prefix = excluded_path[:-2]  # Remove '*/'
                if path.startswith(prefix):
                    return False

        # If path not found in excluded_paths, return True (requires auth)
        return True

    def authorization_header(
        self, request=None
    ) -> str:
        """Get the authorization header from the request

        Args:
            request: The Flask request object

        Returns:
            Value of Authorization header or None
        """
        if request is None:
            return None

        # Return the Authorization header value if it exists
        return request.headers.get('Authorization', None)

    def current_user(
        self, request=None
    ) -> TypeVar('User'):
        """Get the current user from the request

        Args:
            request: The Flask request object

        Returns:
            None for now (will be implemented later)
        """
        return None

    def session_cookie(self, request=None):
        """Get session cookie value from request"""
        if request is None:
            return None

        # More explicit environment variable handling
        session_name = os.environ.get('SESSION_NAME')
        if session_name is None:
            session_name = '_my_session_id'

        # Extra safety check for cookies attribute
        if not hasattr(request, 'cookies'):
            return None

        return request.cookies.get(session_name)
