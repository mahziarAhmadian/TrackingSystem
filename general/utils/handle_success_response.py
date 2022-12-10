from rest_framework import serializers
from general.models import Response
from core import settings
from general.utils.responses import responses


class SuccessSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField('get_details')
    statusCode = serializers.IntegerField(source='status_code')

    class Meta:
        model = Response
        fields = ('summary', 'statusCode', 'details')

    def get_details(self, response):
        return {
            'en': response.english_details,
            'fa': response.farsi_details
        }

# ----------------------------------------------------------------------------------

# generate proper response message

def handle_response_from_db(keyword):
    try:
        response = Response.objects.get(summary=keyword)
    except:
        keyword = 'UNKNOWN'
        response = Response.objects.get(summary=keyword)

    response_data = SuccessSerializer(response).data
    return response_data


def format_response(response):
    return {
        'summary': response.get('summary'),
        'statusCode': response.get('status_code'),
        'details': {
            'en': response.get('english_details'),
            'fa': response.get('farsi_details')
        }
    }


def handle_response_from_ram(keyword):
    response = responses.get(keyword)
    if response is None:
        keyword = 'OPERATION_DONE'
        response = responses.get(keyword)
    return format_response(response)


def generate_response(keyword, **kwargs):
    if settings.HANDLE_ERROR_FROM == "RAM":
        return handle_response_from_ram(keyword=keyword)
    else:
        return handle_response_from_db(keyword=keyword)
        