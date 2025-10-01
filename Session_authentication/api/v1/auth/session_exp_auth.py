#!/usr/bin/env python3
""" SessionExpAuth class
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """Session authentication with expiration"""

    def __init__(self):
        """Initialize SessionExpAuth"""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session with expiration

        Args:
            user_id: User ID to create session for

        Returns:
            Session ID if successful, None otherwise
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Create session dictionary with user_id and creation time
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get User ID based on Session ID with expiration check

        Args:
            session_id: Session ID to look up

        Returns:
            User ID if session exists and not expired, None otherwise
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        # If session_duration is 0 or negative, return user_id (no expiration)
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        # Check if created_at exists in session dictionary
        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        # Check if session has expired
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            # Session expired, remove it
            del self.user_id_by_session_id[session_id]
            return None

        return session_dict.get('user_id')
