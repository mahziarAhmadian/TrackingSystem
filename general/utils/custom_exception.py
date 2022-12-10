from rest_framework.exceptions import APIException, _get_error_details
from rest_framework import status


class CustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid input.'
    default_code = 'invalid'
    default_summary = 'Unknown'
    default_extra_fields = {}

    def __init__(self, error_summary=None, extra_fields=None, code=None):
        if error_summary is None:
            error_summary = self.default_summary
        if extra_fields is None:
            extra_fields = self.default_extra_fields
        if code is None:
            code = self.default_code

        detail = {
            'summary': error_summary,
            'extra_fields': extra_fields
        }

        self.detail = _get_error_details(detail, code)
