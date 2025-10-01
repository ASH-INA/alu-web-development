#!/usr/bin/env python3
""" Authentication module for user authentication service
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize Auth instance with database connection"""
        self._db = DB()

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt

        Args:
            password: The password string to hash

        Returns:
            A salted hash of the password as a string
        """
        return bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')

    def register_user(self, email: str, password: str):
        """Register a new user

        Args:
            email: User's email address
            password: User's password

        Returns:
            User object if registration successful
            
        Raises:
            ValueError: If user already exists with the given email
        """
        try:
            # Check if user already exists
            self._db.find_user_by(email=email)
            # If no exception is raised, user exists
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User doesn't exist, proceed with registration
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
