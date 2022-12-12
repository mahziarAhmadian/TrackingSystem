from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.serializers.user_serializer import UserSerializer, ProfileSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from user.models import User


class UserAPI(APIView):
    serializer_class = UserSerializer

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

    def field_check(self, input_data, required_fields=None, required_field=None):
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

    def put(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        owner_type = self.check_owner_type(input_data)
        required_fields = ['Notes', 'profile_update']
        self.field_check(input_data, required_fields)
        if input_data.get('profile_update'):
            profile_required_fields = ['Email', 'FirstName', 'LastName', 'ZipCode', 'NationalId', 'Information']
            self.field_check(input_data, profile_required_fields)
        if owner_type == 'Other':
            required_fields.append('user_id')
            input_data['MethodType'] = 'One'
            user = self.method_type_check(input_data)
        if input_data.get('profile_update'):
            profile_serializer = ProfileSerializer(user.profile, data=input_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
        serializer = self.serializer_class(user, data=input_data)
        if serializer.is_valid():
            serializer.save()
            data = generate_response(keyword='USER_UPDATED')
            return Response(data, status=data.get('statusCode'))
        else:
            message = {
                "Message": " Not Success ."
            }
            return Response(data=message)

    def patch(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        owner_type = self.check_owner_type(input_data)
        if owner_type == 'Other':
            self.check_user_permission(user=user, user_permission_name='EditUser')
            input_data['MethodType'] = 'One'
            other_user = self.method_type_check(input_data)
            user = other_user
        self.field_check(input_data=input_data, required_field='profile_update')
        if input_data.get('profile_update'):
            profile = user.profile
            if profile is not None:
                profile_serializer = ProfileSerializer(profile, data=input_data, partial=True)
                if profile_serializer.is_valid():
                    profile_serializer.save()
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
                user_info = self.serializer_class(user, many=True).data
                user_info.append({"all_users_count": user.count()})
            else:
                user_info = self.serializer_class(user).data
            data = generate_response(keyword='OPERATION_DONE')
            data['userInfo'] = user_info
            return Response(data, status=data.get('statusCode'))
        return Response(data={"message": "Test"})

    def delete(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        owner = self.check_owner_type(input_data)
        if owner == 'Self':
            if user.profile is not None:
                user.profile.delete()
            else:
                user.delete()
        if owner == 'Other':
            self.check_user_permission(user=user, user_permission_name='DeleteUser')
            if 'user_id' not in input_data:
                errors = []
                extra_fields = {
                    'errorList': errors,
                    'required_field': 'user_id'
                }
                raise CustomException(error_summary='FIELD_REQUIRED', extra_fields=extra_fields)
            user_object = self.get_object(user_id=input_data.get('user_id'))
            if user_object.profile is not None:
                user_object.profile.delete()
            else:
                user_object.delete()
        data = generate_response(keyword='USER_DELETED')
        return Response(data, status=data.get('statusCode'))
