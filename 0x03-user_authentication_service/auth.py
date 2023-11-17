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


def _hash_password(password: str) -> bytes:
    """salted hash of password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


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
