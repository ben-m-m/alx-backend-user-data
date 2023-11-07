#!/usr/bin/env python
"""This class is the template for all authentication system to implement.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        return False

    def authorization_header(self, request=None) -> str:
        pass

    def current_user(self, request=None) -> TypeVar('User'):
        pass
