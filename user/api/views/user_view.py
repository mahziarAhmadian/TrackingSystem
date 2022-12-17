from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.serializers.user_serializer import UserSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from user.models import User, UserProfile
from user.api.utils import check_field, invalid_error, paginator
from user.api.serializers.user_profile_srializer import UserProfileSerializer


class UserAPI(APIView):
    serializer_class = UserSerializer
    pagination_class = paginator.CustomPaginator
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()

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

    def put(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        owner_type = self.check_field.check_owner_type(input_data)
        required_fields = ['Notes', 'profile_update']
        self.check_field.check_field(input_data, required_fields)
        if input_data.get('profile_update'):
            profile_required_fields = ['Email', 'FirstName', 'LastName', 'ZipCode', 'NationalId', 'Information']
            self.check_field.check_field(input_data, profile_required_fields)
        if owner_type == 'Other':
            user_id = self.check_field.check_field(input_data=input_data, required_field='userId')
            user = self.get_object(user_id=user_id)
        if input_data.get('profile_update'):
            if user.profile is not None:
                profile_serializer = UserProfileSerializer(user.profile, data=input_data)
            else:
                profile_serializer = UserProfileSerializer(data=input_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                user_profile_instance = UserProfile.objects.get(id=profile_serializer.data.get('id'))
                user.profile = user_profile_instance
            else:
                self.invalid_error.invalid_serializer(profile_serializer.errors)
        serializer = self.serializer_class(user, data=input_data)
        if serializer.is_valid():
            serializer.save()
            data = generate_response(keyword='USER_UPDATED')
            return Response(data, status=data.get('statusCode'))
        else:
            self.invalid_error.invalid_serializer(serializer.errors)

    def patch(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        owner_type = self.check_field.check_owner_type(input_data)
        if owner_type == 'Other':
            self.check_field.check_user_permission(user=user, user_permission_name='EditUser')
            input_data['MethodType'] = 'One'
            other_user = self.check_field.check_field(input_data=input_data, required_field='UserID')
            user = self.get_object(user_id=other_user)
        self.check_field.check_field(input_data=input_data, required_field='ProfileUpdate')
        if input_data.get('ProfileUpdate'):
            profile = user.profile
            if profile is not None:
                profile_serializer = UserProfileSerializer(profile, data=input_data, partial=True)
                if not profile_serializer.is_valid():
                    self.invalid_error.invalid_serializer(serializer_error=profile_serializer.errors)
                profile_serializer.save()
            else:
                check_fields = ['Email', 'FirstName', 'LastName', 'ZipCode', 'NationalId', 'Information', ]
                for field in check_fields:
                    if field not in input_data:
                        input_data[field] = None
                profile_serializer = UserProfileSerializer(data=input_data)
                if not profile_serializer.is_valid():
                    self.invalid_error.invalid_serializer(serializer_error=profile_serializer.errors)
                profile_serializer.save()
                user_profile_instance = UserProfile.objects.get(id=profile_serializer.data.get('id'))
                user.profile = user_profile_instance
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if not serializer.is_valid():
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)
        serializer.save()
        data = generate_response(keyword='USER_UPDATED')
        return Response(data, status=data.get('statusCode'))

    def get(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        data = generate_response(keyword='OPERATION_DONE')
        owner_type = self.check_field.check_owner_type(input_data=input_data)
        if owner_type == 'Self':
            user_info = self.serializer_class(request.user).data
            data['userInfo'] = user_info
            return Response(data, status=data.get('statusCode'))
        if owner_type == 'Other':
            self.check_field.check_user_permission(user=user, user_permission_name='GetUserDetail')
            method_type = self.check_field.method_type_check(input_data=input_data)
            if method_type == 'All':
                required_fields = ['page', 'count']
                self.check_field.check_field(input_data=input_data, required_fields=required_fields)
                user = self.get_object(user_id=None)
                pagination = self.pagination_class(page=input_data.get('page'), count=input_data.get('count'))
                user_pagination = pagination.pagination_query(query_object=user, order_by_object='create_time')
                user_info = self.serializer_class(user_pagination, many=True).data
                data['allUserCount'] = user.count()
                # user_info.append({"all_users_count": user.count()})
            else:
                user_id = self.check_field.check_field(input_data=input_data, required_field='user_id')
                user = self.get_object(user_id=user_id)
                user_info = self.serializer_class(user).data
            data['userInfo'] = user_info
            return Response(data, status=data.get('statusCode'))

    def delete(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        owner = self.check_field.check_owner_type(input_data)
        if owner == 'Self':
            if user.profile is not None:
                user.profile.delete()
            else:
                user.delete()
        if owner == 'Other':
            self.check_field.check_user_permission(user=user, user_permission_name='DeleteUser')
            user_id = self.check_field.check_field(input_data=input_data, required_field='user_id')
            user_object = self.get_object(user_id=user_id)
            if user_object.profile is not None:
                user_object.profile.delete()
            else:
                user_object.delete()
        data = generate_response(keyword='USER_DELETED')
        return Response(data, status=data.get('statusCode'))
