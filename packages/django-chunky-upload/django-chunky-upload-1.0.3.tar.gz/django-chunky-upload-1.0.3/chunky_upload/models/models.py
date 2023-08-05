#!/usr/bin/env python3
"""Setups a model for tracking Chunky uploads."""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-25"

# stdlib

# django
from django.conf import settings
from django.db import models

# local django
from chunky_upload.models.abstract_models import AbstractChunkedUpload
from chunky_upload.settings import (
    DEFAULT_MODEL_USER_FIELD_BLANK,
    DEFAULT_MODEL_USER_FIELD_NULL,
)

# thirdparty


class ChunkedUpload(AbstractChunkedUpload):
    """
    Default chunked upload model.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chunky_uploads",
        null=DEFAULT_MODEL_USER_FIELD_NULL,
        blank=DEFAULT_MODEL_USER_FIELD_BLANK,
    )
