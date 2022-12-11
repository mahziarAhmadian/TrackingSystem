from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.serializers.user_serializer import UserSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from user.models import User


class UserAPI(APIView):
    serializer_class = UserSerializer

    def get_object(self, user_id=None):
        if user_id is None:
            user = User.objects.all()
        else:
            user = User.objects.get(id=user_id)
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
                'errorList': errors
            }
            raise CustomException(error_summary='FIELD_REQUIRED', extra_fields=extra_fields)
        else:
            return input_data.get('OwnerType')

    def check_user_permission(self, user, user_permission_name):
        if not user.is_staff:
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

    def patch(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        owner_type = self.check_owner_type(input_data)
        if owner_type == 'Other':
            self.check_user_permission(user=user, user_permission_name='EditUser')
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if not serializer.is_valid():
            errors = serializer.errors.get('non_field_errors', None)
            if errors is None:
                errors = []
            extra_fields = {
                'errorList': errors
            }
            raise CustomException(error_summary='INVALID_DATA_RECEIVED', extra_fields=extra_fields)
        serializer.save()
        data = generate_response(keyword='USER_UPDATED')
        return Response(data, status=data.get('statusCode'))

    def get(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        owner_type = self.check_owner_type(input_data)
        if owner_type == 'Self':
            user_info = self.serializer_class(request.user).data
            data = generate_response(keyword='OPERATION_DONE')
            data['userInfo'] = user_info
            return Response(data, status=data.get('statusCode'))
        if owner_type == 'Other':
            self.check_user_permission(user=user, user_permission_name='GetUserDetail')
            user = self.method_type_check(input_data=input_data)
            if input_data['MethodType'] == 'All':
                user_info = self.serializer_class(user, many=True)
            else:
                user_info = self.serializer_class(user)
            data = generate_response(keyword='OPERATION_DONE')
            data['userInfo'] = user_info.data
            return Response(data, status=data.get('statusCode'))
        return Response(data={"message": "Test"})
