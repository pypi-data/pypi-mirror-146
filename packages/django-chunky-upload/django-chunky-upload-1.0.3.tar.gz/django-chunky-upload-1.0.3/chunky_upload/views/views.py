#!/usr/bin/env python3
"""Setups views to handle the ChunkedUpload"""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-24"

# stdlib
import re
from typing import Any, Dict
import uuid

# django
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

# local django
from chunky_upload.constants import http_status
from chunky_upload.models import ChunkedUpload
from chunky_upload.views.base_views import ChunkedUploadBaseView
from chunky_upload.response import Response
from chunky_upload.settings import MAX_BYTES
from chunky_upload.views.helpers import is_authenticated

# thirdparty


class ChunkedUploadView(ChunkedUploadBaseView):
    """
    Uploads large files in multiple chunks. Also, has the ability to resume
    if the upload is interrupted.
    """

    field_name = "file"
    user_field_name = "user"
    content_range_header = "HTTP_CONTENT_RANGE"
    content_range_pattern = re.compile(
        r"^bytes (?P<start>\d+)-(?P<end>\d+)/(?P<total>\d+)$"
    )
    max_bytes = MAX_BYTES  # Max amount of data that can be uploaded
    # If `fail_if_no_header` is True, an exception will be raised if the
    # content-range header is not found. Default is False to match Jquery File
    # Upload behavior (doesn't send header if the file is smaller than chunk)
    fail_if_no_header = False

    model = ChunkedUpload

    def get_extra_attrs(self, request: HttpRequest) -> Dict[str, Any]:
        """
        Extra attribute values to be passed to the new ChunkedUpload instance.
        Should return a dictionary-like object.
        """
        attrs = {}
        if (
            hasattr(self.model, self.user_field_name)
            and hasattr(request, "user")
            and is_authenticated(request.user)
        ):
            attrs[self.user_field_name] = request.user
        return attrs

    def get_max_bytes(self, request):
        """
        Used to limit the max amount of data that can be uploaded. `None` means
        no limit.
        You can override this to have a custom `max_bytes`, e.g. based on
        logged user.
        """

        return self.max_bytes

    def get_response_data(self, chunked_upload, request):
        """
        Data for the response. Should return a dictionary-like object.
        """
        return {
            "upload_id": chunked_upload.upload_id,
            "offset": chunked_upload.offset,
            "expires": chunked_upload.expires_on,
        }

    def _post(self, request: HttpRequest, upload_id: uuid = None, *args, **kwargs):
        if upload_id is None:
            chunked_upload = self._put_chunk(request)
            self._save(chunked_upload)
        else:
            # Grab the chunked upload
            chunked_upload = get_object_or_404(ChunkedUpload, upload_id=upload_id)

        request_data = self.parse_request_body(request)

        md5 = request_data.get("md5")

        self.md5_check(chunked_upload, md5)

        # Mark the upload as complete
        chunked_upload.complete_upload()

        self.complete_upload(chunked_upload)

        # Create Response
        return Response(
            self.get_response_data(chunked_upload=chunked_upload, request=request),
            status=http_status.HTTP_200_OK,
        )

    def _put(self, request, upload_id: uuid = None, *args, **kwargs):
        try:
            self.validate(request)

            chunked_upload = self._put_chunk(request)

            self._save(chunked_upload)

            return Response(
                self.get_response_data(chunked_upload=chunked_upload, request=request),
                status=http_status.HTTP_200_OK,
            )
        except ValidationError as err:
            return Response(err, status=http_status.HTTP_400_BAD_REQUEST)
