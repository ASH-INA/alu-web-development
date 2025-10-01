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

    def create_session(self, email: str) -> str:
        """Create a session for a user

        Args:
            email: User's email address

        Returns:
            Session ID if user exists, None otherwise
        """
        try:
            # Find user by email
            user = self._db.find_user_by(email=email)
            
            # Generate session ID
            session_id = _generate_uuid()

            # Update user's session_id in database
            self._db.update_user(user.id, session_id=session_id)

            return session_id

        except NoResultFound:
            # User not found
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get user from session ID

        Args:
            session_id: Session ID to look up

        Returns:
            User object if found, None otherwise
        """
        if session_id is None:
            return None

        try:
            # Find user by session_id
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            # User not found
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy user session by setting session_id to None

        Args:
            user_id: ID of the user whose session to destroy
        """
        try:
            # Update user's session_id to None
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            # User not found - do nothing as specified
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token for a user

        Args:
            email: User's email address
            
        Returns:
            Reset token string

        Raises:
            ValueError: If user does not exist
        """
        try:
            # Find user by email
            user = self._db.find_user_by(email=email)

            # Generate reset token
            reset_token = _generate_uuid()
            
            # Update user's reset_token in database
            self._db.update_user(user.id, reset_token=reset_token)

            return reset_token

        except NoResultFound:
            # User not found
            raise ValueError(f"User with email {email} does not exist")

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password using reset token

        Args:
            reset_token: Reset token to validate
            password: New password to set

        Raises:
            ValueError: If reset token is invalid
        """
        try:
            # Find user by reset_token
            user = self._db.find_user_by(reset_token=reset_token)

            # Hash the new password
            hashed_password = _hash_password(password)

            # Update user's password and clear reset_token
            self._db.update_user(
                user.id, 
                hashed_password=hashed_password,
                reset_token=None
            )

        except NoResultFound:
            # Invalid reset token
            raise ValueError("Invalid reset token")
