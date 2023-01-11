from rest_framework.views import APIView
from rest_framework.response import Response
from ..seializers.permissions_serializer import PermissionSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from ...models import Permission
from user.api.utils import check_field, invalid_error, paginator
from user.api.serializers.user_profile_srializer import UserProfileSerializer
from ..utils import system_permissions


class PermissionAPI(APIView):
    serializer_class = PermissionSerializer
    pagination_class = paginator.CustomPaginator
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()
    system_permissions = system_permissions.SystemPermissions()

    def get_object(self, permission_id=None, ):
        if permission_id is None:
            all_permissions = Permission.objects.all()
        return all_permissions

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new project .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new project to system .
        self.check_field.check_user_permission(user=user, user_permission_name='AddPermissions')
        # check for required field should be in input data .
        required_fields = ['AutoAddPermissions', 'AutoAddForUser']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        # get all system permission
        all_permission_in_system = self.get_object()
        all_permission_in_system_title = list(all_permission_in_system.values('title'))
        all_permission_in_system_list = []
        for permission_name in all_permission_in_system_title:
            all_permission_in_system_list.append(permission_name['title'])

        def serializer_create(data):
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()

        def Diff(li1, li2):
            li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
            return li_dif

        if input_data.get('AutoAddPermissions'):
            permissions_list = self.system_permissions.all_permissions()
            for permissions in permissions_list:
                permissions_item = permissions_list[permissions]
                for permission in permissions_item:
                    if permission not in all_permission_in_system_list:
                        title = permission
                        description = f'this permission is use for {permission}'
                        data = {
                            'title': title,
                            'description': description
                        }
                        serializer_create(data=data)
            if input_data.get('AutoAddForUser'):
                user_permissions = user.permissions.all().values('title')
                user_permissions_list = []
                for permission_name in user_permissions:
                    user_permissions_list.append(permission_name['title'])
                permission_user_dont_have = Diff(li1=all_permission_in_system_list, li2=user_permissions_list)
                for permissionName in permission_user_dont_have:
                    permissionId = all_permission_in_system.get(title=permissionName)
                    user.permissions.add(permissionId.id)
            data = generate_response(keyword='PERMISSIONS_CREATED')
            return Response(data, status=data.get('statusCode'))

        elif input_data.get('AutoAddPermissions') is False:
            required_fields = ['title', 'description']
            self.check_field.check_field(input_data=input_data, required_fields=required_fields)
            data = {
                'title': input_data.get('title'),
                'description': input_data.get('description'),
            }
            serializer_create(data=data)
            data = generate_response(keyword='PERMISSIONS_CREATED')
            return Response(data, status=data.get('statusCode'))
