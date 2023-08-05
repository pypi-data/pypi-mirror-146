#!/usr/bin/env python3
"""Setups a helper function to check if the user is authenticated."""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-24"

# stdlib

# django

# local django

# thirdparty


def is_authenticated(user) -> bool:
    return user.is_authenticated
