from rest_framework.views import APIView
from rest_framework.response import Response
from tracking_devices.api.serializers.module_serializer import ModuleSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from tracking_devices.models import Module
from general.utils import check_field, invalid_error, paginator


class ModuleView(APIView):
    serializer_class = ModuleSerializer
    pagination_class = paginator.CustomPaginator
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()

    def get_object(self, module_id, filters=None):
        if module_id is None:
            filters = {k: v for k, v in filters.items() if v is not None}
            module_objects = Module.objects.filter(**filters)
            return module_objects
        else:
            try:
                module_object = Module.objects.get(id=module_id)
            except:
                errors = []
                extra_fields = {
                    'errorList': errors
                }
                raise CustomException(error_summary='MODULE_NOT_EXISTS', extra_fields=extra_fields)
            return module_object

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='AddModule')
        # check for required field should be in input data .
        required_fields = ['name', 'serialNumber', 'information']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)

        serializer = self.serializer_class(data=input_data, context={'request': request})
        if not serializer.is_valid():
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)
        serializer.save()
        data = generate_response(keyword='Module_ADDED')
        return Response(data=data, status=data.get('statusCode'))

    def patch(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='EditModule')
        # check for required field should be in input data .
        self.check_field.check_field(input_data, required_field='moduleId')
        module_obj = self.get_object(module_id=input_data.get('moduleId'))
        serializer = ModuleSerializer(module_obj, data=input_data, context={'request': request}, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = generate_response(keyword='MODULE_UPDATED')
            return Response(data, status=data.get('statusCode'))
        else:
            self.invalid_error.invalid_serializer(serializer.errors)

    def put(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='EditModule')
        # check for required field should be in input data .
        required_fields = ['moduleId', 'name', 'information']
        self.check_field.check_field(input_data, required_fields=required_fields)
        module_obj = self.get_object(module_id=input_data.get('moduleId'))
        module_serial_number = module_obj.serial_number
        input_data['serialNumber'] = module_serial_number
        serializer = ModuleSerializer(module_obj, data=input_data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            data = generate_response(keyword='MODULE_UPDATED')
            return Response(data, status=data.get('statusCode'))
        else:
            print(serializer.errors)
            self.invalid_error.invalid_serializer(serializer.errors)

    def delete(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='DeleteModule')
        # check for required field should be in input data .
        self.check_field.check_field(input_data, required_field='moduleId')
        module_obj = self.get_object(module_id=input_data.get('moduleId'))
        module_obj.delete()
        data = generate_response(keyword='MODULE_DELETED')
        return Response(data, status=data.get('statusCode'))

    def get(self, request, *args, **kwargs):
        # input_data = request.data
        input_data = request.GET
        #return Response(input_data, status=200)
        user = request.user
        data = generate_response(keyword='OPERATION_DONE')
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='GetModule')
        # check method type for get_one or get_all .
        method_type = self.check_field.method_type_check(input_data=input_data)
        if method_type == 'All':
            required_fields = ['page', 'count', 'name', 'serialNumber']
            # check for required fields should be in input data .
            self.check_field.check_field(input_data, required_fields=required_fields)
            # filters for get_all
            filters = {
                'name__icontains': input_data.get('name'),
                'serial_number': input_data.get('serialNumber'),
            }
            modules_obj = self.get_object(module_id=None, filters={})
            pagination = self.pagination_class(page=int(input_data.get('page')), count=int(input_data.get('count')))
            module_pagination = pagination.pagination_query(query_object=modules_obj, order_by_object='create_time')
            module_info = self.serializer_class(module_pagination, many=True).data
            data['allUserCount'] = modules_obj.count()
        else:
            # check for required field should be in input data .
            self.check_field.check_field(input_data, required_field='moduleId')
            module_obj = self.get_object(module_id=input_data.get('moduleId'))
            module_info = self.serializer_class(module_obj).data
        data['moduleInfo'] = module_info
        return Response(data, status=data.get('statusCode'))
