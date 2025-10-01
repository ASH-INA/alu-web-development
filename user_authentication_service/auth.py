#!/usr/bin/env python3
""" Authentication module for user authentication service
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(
        password.encode('utf-8'), bcrypt.gensalt()
    ).decode('utf-8')


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize Auth instance with database connection"""
        self._db = DB()

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return _hash_password(password)

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = self._hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user
