#!/usr/bin/env python3
"""
 takes in a password string arguments and returns bytes.
 The returned bytes is a salted hash of the input password,
 hashed with bcrypt.hashpw
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """salted hash of password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID.

    Returns:
        str: String representation of the generated UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email (str): User's email
            password (str): User's password

        Returns:
            User: User object representing the registered user
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
        raise ValueError(f'User {email} already exists.')

    def valid_login(self, email: str, password: str) -> bool:
        """
        expect email and password required arguments and return a boolean.
        Try locating the user by email.
        If it exists, check the password with bcrypt.checkpw.
        If it matches return True. In any other case, return False
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for the user and return the session ID.

        Args:
            email (str): User's email.

        Returns:
            str: Session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                user.session_id = session_id
                self._db._session.commit()
                return session_id
            else:
                raise ValueError

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id) -> str:
        """
        takes a single session_id string argument and
        returns the corresponding User or None.
        If the session ID is None or no user is found,
        return None. Otherwise return the corresponding user.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session for the user with the provided user_id.

        Args:
            user_id (int): ID of the user.

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Get a reset password token for the user with the given email.

        Args:
            email (str): User's email.

        Returns:
            str: Reset password token.
        """
        user = self._db.find_user_by(email=email)
        if user:
            reset_token = _generate_uuid()
            user.reset_token = reset_token
            self._db.session.commit()
            return reset_token
        else:
            raise ValueError
