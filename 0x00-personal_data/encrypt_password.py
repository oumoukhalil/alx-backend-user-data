#!/usr/bin/env python3
"""password encrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hash password

    Arguments
    ---------
    password: str

    Return
    ------
    str
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf8'), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check if the passwor is mached with
    the hashed_password

    Arguments
    ---------
    hashed_password: bytes
    password: str

    Return
    ------
    bool
    """
    checked = bcrypt.checkpw(password.encode('utf8'), hashed_password)
    return checked
