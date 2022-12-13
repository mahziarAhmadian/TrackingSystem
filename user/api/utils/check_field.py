from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.serializers.user_serializer import UserSerializer, ProfileSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from user.models import User


class CheckField:
    def __init__(self, field_name=None):
        self.field_name = field_name

    def get_object(self, user_id=None):
        if user_id is None:
            user = User.objects.all()
        else:
            try:
                user = User.objects.get(id=user_id)
            except:
                errors = []
                extra_fields = {
                    'errorList': errors
                }
                raise CustomException(error_summary='USER_NOT_EXISTS', extra_fields=extra_fields)
        return user

    def method_type_check(self, input_data):
        if 'MethodType' not in input_data:
            errors = []
            extra_fields = {
                'errorList': errors,
                'required_field': 'MethodType'
            }
            raise CustomException(error_summary='FIELD_REQUIRED', extra_fields=extra_fields)
        method_type = input_data.get('MethodType')
        if method_type == 'All':
            user = self.get_object()
        elif method_type == 'One':
            if 'user_id' not in input_data:
                errors = []
                extra_fields = {
                    'errorList': errors,
                    'required_field': 'user_id'
                }
                raise CustomException(error_summary='FIELD_REQUIRED', extra_fields=extra_fields)
            user_id = input_data.get('user_id')
            user = self.get_object(user_id=user_id)
        return user

    def check_owner_type(self, input_data):
        if 'OwnerType' not in input_data:
            errors = []
            extra_fields = {
                'errorList': errors,
                'required_field': 'OwnerType'
            }
            raise CustomException(error_summary='FIELD_REQUIRED', extra_fields=extra_fields)
        else:
            return input_data.get('OwnerType')

    def check_user_permission(self, user, user_permission_name):
        if not user.is_superuser:
            errors = []
            extra_fields = {
                'errorList': errors
            }
            raise CustomException(error_summary='PERMISSION_DENIED', extra_fields=extra_fields)
        try:
            user_permission = user.permissions.get(title=user_permission_name)
        except:
            errors = []
            extra_fields = {
                'errorList': errors
            }
            raise CustomException(error_summary='PERMISSION_DENIED', extra_fields=extra_fields)

    def check_field(self, input_data, required_fields=None, required_field=None):
        if required_field is not None:
            if required_field not in input_data:
                errors = []
                extra_fields = {
                    'errorList': errors,
                    'required_field': required_field
                }
                raise CustomException(error_summary='FIELD_REQUIRED', extra_fields=extra_fields)
        if required_fields is not None:
            for field in required_fields:
                if field not in input_data:
                    errors = []
                    extra_fields = {
                        'errorList': errors,
                        'required_field': field
                    }
                    raise CustomException(error_summary='FIELD_REQUIRED', extra_fields=extra_fields)
