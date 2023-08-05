#!/usr/bin/env python3
"""Setups custom signals to notify users of certain events."""

__author__ = "Jaryd Rester"
__copyright__ = "2022-04-08"

# stdlib

# django
from django.dispatch import Signal

# local django

# thirdparty

chunky_upload_complete = Signal()
