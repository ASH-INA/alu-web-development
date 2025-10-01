#!/usr/bin/env python3
""" Database class for user authentication service
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """Database class for handling user operations"""

    def __init__(self):
        """Initialize database connection and create tables"""
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Get database session"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
            email: User's email address
            hashed_password: Hashed password for the user

        Returns:
            User object that was created
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments

        Args:
            **kwargs: Arbitrary keyword arguments for filtering

        Returns:
            User object if found

        Raises:
            NoResultFound: When no user is found
            InvalidRequestError: When wrong query arguments are passed
        """
        if not kwargs:
            raise InvalidRequestError("No filter criteria provided")

        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No user found with the given criteria")
            return user
        except NoResultFound:
            # Re-raise NoResultFound without modification
            raise
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes

        Args:
            user_id: ID of the user to update
            **kwargs: Arbitrary keyword arguments for attributes to update

        Returns:
            None

        Raises:
            ValueError: If an argument does not correspond to a user attribute
        """
        # Find the user by ID
        user = self.find_user_by(id=user_id)

        # List of valid user attributes
        valid_attributes = [
            'email',
            'hashed_password',
            'session_id',
            'reset_token'
        ]

        # Check if all kwargs are valid user attributes
        for key in kwargs:
            if key not in valid_attributes:
                raise ValueError(f"Invalid attribute: {key}")

        # Update user attributes
        for key, value in kwargs.items():
            setattr(user, key, value)

        # Commit changes to database
        self._session.commit()
