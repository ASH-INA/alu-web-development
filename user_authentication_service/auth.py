#!/usr/bin/env python3
""" Authentication module for user authentication service
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Hash a password using bcrypt

    Args:
        password: The password string to hash

    Returns:
        A salted hash of the password as a string
    """
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')


def _generate_uuid() -> str:
    """Generate a new UUID

    Returns:
        String representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize Auth instance with database connection"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
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
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login credentials

        Args:
            email: User's email address
            password: User's password to validate

        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            # Find user by email
            user = self._db.find_user_by(email=email)

            # Check if password matches
            password_bytes = password.encode('utf-8')
            hashed_password_bytes = user.hashed_password.encode('utf-8')

            return bcrypt.checkpw(password_bytes, hashed_password_bytes)

        except NoResultFound:
            # User not found
            return False
