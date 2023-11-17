#!/usr/bin/env python3
"""
 takes in a password string arguments and returns bytes.
 The returned bytes is a salted hash of the input password,
 hashed with bcrypt.hashpw
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """salted hash of password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
