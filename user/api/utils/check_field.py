from general.utils.custom_exception import CustomException
from .validation import is_type
from user.models.user import User


class CheckField:
    def __init__(self, field_name=None):
        self.field_name = field_name

    def check_field(self, input_data, required_fields=None, required_field=None):
        if required_field is not None:
            if required_field not in input_data:
                errors = []
                extra_fields = {
                    'errorList': errors,
                    'required_field': required_field
                }
                raise CustomException(error_summary='FIELD_REQUIRED', extra_fields=extra_fields)
            else:
                return input_data[required_field]
        if required_fields is not None:
            for field in required_fields:
                if field not in input_data:
                    errors = []
                    extra_fields = {
                        'errorList': errors,
                        'required_field': field
                    }
                    raise CustomException(error_summary='FIELD_REQUIRED', extra_fields=extra_fields)

    def method_type_check(self, input_data, required_field_one_method=None):
        self.check_field(input_data=input_data, required_field='MethodType')
        method_type = input_data.get('MethodType')
        return method_type

    def check_owner_type(self, input_data):
        self.check_field(input_data=input_data, required_field='OwnerType')
        return input_data.get('OwnerType')

    def check_user_permission(self, user, user_permission_name):
        if not user.is_superuser:
            errors = []
            extra_fields = {
                'errorList': errors
            }
            raise CustomException(error_summary='PERMISSION_DENIED', extra_fields=extra_fields)
        try:
            user.permissions.get(title=user_permission_name)
        except:
            errors = []
            extra_fields = {
                'errorList': errors
            }
            raise CustomException(error_summary='PERMISSION_DENIED', extra_fields=extra_fields)

    def check_user_type(self, user, required_type_english_name):
        if user.type is None:
            errors = []
            extra_fields = {
                'errorList': errors,
            }
            raise CustomException(error_summary='USER_DONT_SET_TYPE', extra_fields=extra_fields)

        if user.type.english_name not in required_type_english_name:
            errors = []
            extra_fields = {
                'errorList': errors,
            }
            raise CustomException(error_summary='USER_TYPE_ERROR', extra_fields=extra_fields)

    def check_user_exist(self, user_id):
        try:
            user_obj = User.objects.get(id=user_id)
        except:
            errors = []
            extra_fields = {
                'errorList': errors
            }
            raise CustomException(error_summary='USER_NOT_EXISTS', extra_fields=extra_fields)
        return user_obj
