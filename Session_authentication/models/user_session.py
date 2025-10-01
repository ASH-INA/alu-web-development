#!/usr/bin/env python3
""" UserSession model
"""
from models.base import Base


class UserSession(Base):
    """UserSession class for storing session data in database"""

    def __init__(self, *args, **kwargs):
        """Initialize UserSession instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', '')
        self.session_id = kwargs.get('session_id', '')
