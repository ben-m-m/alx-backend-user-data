#!/usr/bin/env python
"""This class is the template for all authentication system to implement.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return False"""
        return False

    def authorization_header(self, request=None) -> str:
        """returns None - request will be the Flask request object"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request will be the Flask request object"""
        return None
