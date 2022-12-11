from general.models import Response as ResponseModel
from rest_framework import serializers
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, _get_error_details
from rest_framework import status
from rest_framework.response import Response
from general.utils.responses import responses
from core import settings


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


# serialized Error


class ErrorSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField('get_details')
    statusCode = serializers.IntegerField(source='status_code')
    errorCode = serializers.IntegerField(source='error_code')

    class Meta:
        model = ResponseModel
        fields = ('summary', 'statusCode', 'errorCode', 'details')

    def get_details(self, error):
        return {
            'en': error.english_details,
            'fa': error.farsi_details
        }


# ----------------------------------------------------------------------------------

# generate proper error message


def handle_error_from_db(keyword):
    try:
        error = ResponseModel.objects.get(summary=keyword)
    except:
        keyword = 'UNKNOWN'
        error = ResponseModel.objects.get(summary=keyword)

    error_data = ErrorSerializer(error).data
    return error_data


def format_error(error):
    return {
        'summary': error.get('summary'),
        'statusCode': error.get('status_code'),
        'errorCode': error.get('error_code'),
        'details': {
            'en': error.get('english_details'),
            'fa': error.get('farsi_details')
        }
    }


def handle_error_from_ram(keyword, required_field):
    # if
    error = responses.get(keyword)
    if error is None:
        keyword = 'UNKNOWN'
        error = responses.get(keyword)
    if required_field is not None:
        error['summary'] = required_field + '_' + 'FIELD_REQUIRED'
        error['english_details'] = f"please enter {required_field} field ."
        error['farsi_details'] = f"لطفا فیلد {required_field} وارد کنید"
    return format_error(error)


def generate_error(keyword, required_field=None, **kwargs):
    if settings.HANDLE_ERROR_FROM == "RAM":
        return handle_error_from_ram(keyword=keyword, required_field=required_field)
    else:
        return handle_error_from_db(keyword=keyword)


# -------------------------------------------------------------------------------------

# custom exception handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    print("response is {}".format(response))
    if response is None:
        # unknown_error = generate_error(keyword='UNKNOWN')
        # return Response(data=unknown_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
    try:
        print(response.data)
        # required_filed = response.data.get('required_filed')
        error_summary = response.data.get('summary')
        extra_fields = response.data.get('extra_fields')
        print(error_summary)
        print(extra_fields)
        if 'required_field' in extra_fields:
            required_field = extra_fields.get('required_field')
        else:
            required_field = None
        main_error = generate_error(keyword=error_summary, required_field=required_field)
        # ----------------------------------------------------------------------
        error_list = extra_fields.get('errorList', None)
        if error_list is not None:
            if len(error_list) > 0:
                error_list_details = list()
                for error_summary in error_list:
                    error_list_details.append(generate_error(keyword=error_summary))
                extra_fields['errorList'] = error_list_details
            else:
                extra_fields = {}
        # else:
        #     extra_fields = {}
        # -------------------------------------------------------------------------
        main_error.update(extra_fields)
        response.status_code = main_error.get('statusCode')
        response.data = main_error
    except:
        pass
    return response
