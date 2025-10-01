#!/usr/bin/env python3
""" User model for authentication service
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """User class for storing user data in database"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __init__(self, email: str, hashed_password: str):
        """Initialize User instance

        Args:
            email: User's email address
            hashed_password: Hashed password for the user
        """
        self.email = email
        self.hashed_password = hashed_password
