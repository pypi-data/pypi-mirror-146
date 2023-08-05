#!/usr/bin/env python3
"""Setups a series of base views"""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-24"

# stdlib
from typing import Dict, Tuple

# django
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

# local django
from chunky_upload.constants import COMPLETE, http_status
from chunky_upload.exceptions import ChunkedUploadError
from chunky_upload.models import AbstractChunkedUpload
from chunky_upload.response import Response
from chunky_upload.views.helpers import is_authenticated

# thirdparty
from ast import literal_eval


class ChunkedUploadBaseView(View):
    """
    Base view for the rest of chunked upload views.
    """

    perform_md5_checksum: bool = True

    def create_chunked_upload(self, save=False, **attrs) -> AbstractChunkedUpload:
        """
        Creates a new AbstractChunkedUpload when required
        :param attrs: various attributes that should be saved in the AbstractChunkedUpload
        :type attrs: Dict[str, Any]

        :return: a new AbstractChunkedUpload to be used
        :rtype: AbstractChunkedUpload
        """
        chunked_upload: AbstractChunkedUpload = self.model(**attrs)

        chunked_upload.file.save(name="", content=ContentFile(b""), save=save)
        # file starts empty
        return chunked_upload

    def get_queryset(self, request: HttpRequest) -> QuerySet[AbstractChunkedUpload]:
        """
        Get (and filter) ChunkedUpload queryset.
        By default, users can only continue uploading their own uploads.
        """
        queryset: QuerySet[AbstractChunkedUpload] = self.model.objects.all()
        if (
            hasattr(self.model, self.user_field_name)
            and hasattr(request, "user")
            and is_authenticated(request.user)
        ):
            queryset = queryset.filter(**{self.user_field_name: request.user})
        return queryset

    def parse_request_body(self, request: HttpRequest) -> Dict:
        json_body = request.body.decode().replace("'", '"')
        dictionary_body = literal_eval(json_body)
        return dictionary_body

    def get_file_from_request(self, request: HttpRequest) -> UploadedFile:
        """Pull the file object from the request.
        :param request: the HttpRequest we are handling
        :type request: HttpRequest

        :raises ChunkedUploadError: an error specifying the request is invalid

        :return: the file the user uploaded attached on the main field_name
        :rtype: UploadedFile
        """
        try:
            json_body = request.body.decode().replace("'", '"')
            dictionary_body = literal_eval(json_body)
            return InMemoryUploadedFile(
                bytes(dictionary_body["file"]),
                size=len(dictionary_body["file"]),
                field_name="test",
                name=dictionary_body["filename"],
                content_type="binary",
                charset="utf-8",
            )

        except KeyError:
            raise ChunkedUploadError(
                status=http_status.HTTP_400_BAD_REQUEST,
                detail=_("No chunk file was submitted"),
            )

    def get_file_range_from_request(
        self, request: HttpRequest, chunk: UploadedFile
    ) -> Tuple[int, int, int, int, int]:
        """Extracts the content range information from the request.
        :param request: the HttpRequest we are handling
        :type request: HttpRequest
        :param chunk: the file we are handling
        :type chunk: UploadedFile

        :raises ChunkedUploadError: an error specifying why the request is invalid

        :return: the file range
        :rtype: Tuple[int, int, int, int, int]
        """
        content_range = request.META.get(self.content_range_header, "")
        match = self.content_range_pattern.match(content_range)
        if match:
            start = int(match.group("start"))
            end = int(match.group("end"))
            total = int(match.group("total"))
        elif self.fail_if_no_header:
            raise ChunkedUploadError(
                status=http_status.HTTP_400_BAD_REQUEST,
                detail="Error in request headers",
            )
        else:
            # Use the whole size when HTTP_CONTENT_RANGE is not provided
            start = 0
            end = chunk.size - 1
            total = chunk.size

        chunk_size = end - start + 1
        max_bytes = self.get_max_bytes(request)

        return (
            start,
            end,
            chunk_size,
            total,
            max_bytes,
        )

    def validate_chunked_upload(self, chunked_upload: AbstractChunkedUpload):
        """
        Check if chunked upload has already expired or is already complete.
        """
        if chunked_upload.expired:
            raise ChunkedUploadError(
                status=http_status.HTTP_410_GONE, detail=_("Upload has expired")
            )
        if chunked_upload.status == COMPLETE:
            raise ChunkedUploadError(
                status=http_status.HTTP_400_BAD_REQUEST,
                detail=_('Upload has already been marked as "COMPLETE"'),
            )

    def get_chunked_upload(
        self, request: HttpRequest, chunk: UploadedFile
    ) -> AbstractChunkedUpload:
        """Get the AbstractChunkedUpload to be used when handling this request.
        :param request: the HttpRequest we are handling
        :type request: HttpRequest
        :param chunk: the file we are handling
        :type chunk: UploadedFile

        :return: the AbstractChunkedUpload to handle the chunk
        :rtype: AbstractChunkedUpload
        """
        upload_id = self.kwargs.get("upload_id")

        if upload_id is not None:
            chunked_upload: AbstractChunkedUpload = get_object_or_404(
                self.get_queryset(request), upload_id=upload_id
            )
            self.validate_chunked_upload(chunked_upload)
        else:
            attrs = {"filename": chunk.name}
            attrs.update(self.get_extra_attrs(request))
            chunked_upload = self.create_chunked_upload(save=False, **attrs)

        return chunked_upload

    def _put_chunk(self, request: HttpRequest):
        chunk = self.get_file_from_request(request)

        start, _, chunk_size, total, max_bytes = self.get_file_range_from_request(
            request, chunk
        )

        chunked_upload = self.get_chunked_upload(request, chunk)

        if max_bytes is not None and total > max_bytes:
            raise ChunkedUploadError(
                status=http_status.HTTP_400_BAD_REQUEST,
                detail="Size of file exceeds the limit (%s bytes)" % max_bytes,
            )
        if chunked_upload.offset != start:
            raise ChunkedUploadError(
                status=http_status.HTTP_400_BAD_REQUEST,
                detail="Offsets do not match",
                offset=chunked_upload.offset,
            )
        if chunk.size != chunk_size:
            raise ChunkedUploadError(
                status=http_status.HTTP_400_BAD_REQUEST,
                detail="File size doesn't match headers",
            )

        chunked_upload.append_chunk(chunk, chunk_size=chunk_size, save=False)

        return chunked_upload

    def validate(self, request):
        """
        Placeholder method to define extra validation.
        Must raise ChunkedUploadError if validation fails.
        """
        pass

    def get_response_data(self, chunked_upload, request):
        """
        Data for the response. Should return a dictionary-like object.
        Called *only* if POST is successful.
        """
        return {}

    def pre_save(self, chunked_upload, request, new=False):
        """
        Placeholder method for calling before saving an object.
        May be used to set attributes on the object that are implicit
        in either the request, or the url.
        """

    def save(self, chunked_upload, request, new=False):
        """
        Method that calls save(). Overriding may be useful is save() needs
        special args or kwargs.
        """
        chunked_upload.save()

    def post_save(self, chunked_upload, request, new=False):
        """
        Placeholder method for calling after saving an object.
        """

    def _save(self, chunked_upload):
        """
        Wraps save() method.
        """
        new = chunked_upload.id is None
        self.pre_save(chunked_upload, self.request, new=new)
        self.save(chunked_upload, self.request, new=new)
        self.post_save(chunked_upload, self.request, new=new)

    def check_permissions(self, request):
        """
        Grants permission to start/continue an upload based on the request.
        """
        if hasattr(request, "user") and not is_authenticated(request.user):
            raise ChunkedUploadError(
                status=http_status.HTTP_403_FORBIDDEN,
                detail="Authentication credentials were not provided",
            )

    def md5_check(self, chunk_upload: AbstractChunkedUpload, md5: str):
        if self.perform_md5_checksum and md5 != chunk_upload.md5:
            raise ChunkedUploadError(
                status=http_status.HTTP_400_BAD_REQUEST,
                detail=_("md5 checksum does not match"),
            )

    def _post(self, request, *args, **kwargs):
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        """
        try:
            self.check_permissions(request)
            return self._post(request, *args, **kwargs)
        except ChunkedUploadError as error:
            return Response(error.data, status=error.status_code)

    def _put(self, request, *args, **kwargs):
        raise NotImplementedError

    def put(self, request, *args, **kwargs):
        try:
            self.check_permissions(request)
            return self._put(request, *args, **kwargs)
        except ChunkedUploadError as error:
            return Response(error.data, status=error.status_code)

    def complete_upload(self, chunked_upload: AbstractChunkedUpload):
        """Placeholder method to call after completing an upload"""
