#!/usr/bin/env python3
""" SessionAuth class
"""
from api.v1.auth.auth import Auth
import uuid
from typing import TypeVar


class SessionAuth(Auth):
    """Session authentication class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id

        Args:
            user_id: User ID to create session for
   
        Returns:
            Session ID if successful, None otherwise
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        # Generate Session ID using uuid4
        session_id = str(uuid.uuid4())

        # Store user_id with session_id as key
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get User ID based on Session ID

        Args:
            session_id: Session ID to look up

        Returns:
            User ID if session exists, None otherwise
        """
        if session_id is None:
            return None

        if not isinstance(session_id, str):
            return None

        # Use .get() to safely retrieve user_id from dictionary
        return self.user_id_by_session_id.get(session_id)
