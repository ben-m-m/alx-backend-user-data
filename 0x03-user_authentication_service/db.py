#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database

        Args:
            email (str): User's email
            hashed_password (str): Hashed password

        Returns:
            User: User object representing the added user
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
            return new_user
        except Exception as e:
            print("Error adding new user: {e}")
            self._session.rollback()
            return None

    def find_user_by(self, **kwargs) -> User:
        """
        returns the first row found in the
        users table as filtered by the method’s input arguments
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound as e:
            raise e
        except InvalidRequestError as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """_summary_

        Args:
            user_id (int): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
        Returns:
            None: _description_
        """
        user = self.find_user_by(id=user_id)
        if not user:
            raise ValueError

        valid_keys = ['email', 'hashed_password']
        for key, value in kwargs.items():
            if key not in valid_keys:
                raise ValueError
            setattr(user, key, value)

        self._session.commit()
        pass
