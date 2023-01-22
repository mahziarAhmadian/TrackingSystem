from rest_framework.views import APIView
from rest_framework.response import Response
from tracking_devices.api.serializers.truck_serializer import TruckSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from tracking_devices.models import Truck
from general.utils import check_field, invalid_error, paginator


class TruckView(APIView):
    serializer_class = TruckSerializer
    pagination_class = paginator.CustomPaginator
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()

    def get_object(self, truck_id=None, filters=None):
        if truck_id is None:
            filters = {k: v for k, v in filters.items() if v is not None}
            truck_objects = Truck.objects.filter(**filters)
            return truck_objects
        else:
            try:
                truck_object = Truck.objects.get(id=truck_id)
            except:
                errors = []
                extra_fields = {
                    'errorList': errors
                }
                raise CustomException(error_summary='TRUCK_NOT_EXISTS', extra_fields=extra_fields)
            return truck_object

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='AddTruck')
        # check for required field should be in input data .
        required_fields = ['name', 'numberPlate', 'model', 'information', 'meterId', 'driverId', 'ownerId']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        serializer = self.serializer_class(data=input_data, context={'request': request})
        if not serializer.is_valid():
            print(serializer.errors)
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)
        serializer.save()
        data = generate_response(keyword='TRUCK_ADDED')
        return Response(data=data, status=data.get('statusCode'))

    def get(self, request, *args, **kwargs):
        #input_data = request.data
        input_data = request.GET
        user = request.user
        data = generate_response(keyword='OPERATION_DONE')
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='GetTruck')
        # check method type for get_one or get_all .
        method_type = self.check_field.method_type_check(input_data=input_data)
        if method_type == 'All':
            required_fields = ['page', 'count', 'name', 'numberPlate', 'model']
            # check for required fields should be in input data .
            self.check_field.check_field(input_data, required_fields=required_fields)
            # filters for get_all
            filters = {
                'name__icontains': input_data.get('name'),
                'numberPlate': input_data.get('numberPlate'),
                'model': input_data.get('model'),
            }
            truck_obj = self.get_object(filters={})
            pagination = self.pagination_class(page=int(input_data.get('page')), count=int(input_data.get('count')))
            module_pagination = pagination.pagination_query(query_object=truck_obj, order_by_object='create_time')
            truck_info = self.serializer_class(module_pagination, many=True).data
            data['allTruckCount'] = truck_obj.count()
        else:
            # check for required field should be in input data .
            self.check_field.check_field(input_data, required_field='truckId')
            truck_obj = self.get_object(truck_id=input_data.get('truckId'))
            truck_info = self.serializer_class(truck_obj).data
        data['truckInfo'] = truck_info
        return Response(data, status=data.get('statusCode'))

    def patch(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='EditTruck')
        # check for required field should be in input data .
        self.check_field.check_field(input_data, required_field='truckId')
        truck_obj = self.get_object(truck_id=input_data.get('truckId'))
        serializer = self.serializer_class(truck_obj, data=input_data, context={'request': request}, partial=True)

        if serializer.is_valid():
            serializer.update(instance=truck_obj, validated_data=input_data)
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
        self.check_field.check_user_permission(user=user, user_permission_name='EditTruck')
        # check for required field should be in input data .
        required_fields = ['truckId', 'name', 'model', 'information']
        self.check_field.check_field(input_data, required_fields=required_fields)
        truck_obj = self.get_object(truck_id=input_data.get('truckId'))
        serializer = self.serializer_class(truck_obj, data=input_data, context={'request': request}, partial=True)

        if serializer.is_valid():
            serializer.update(instance=truck_obj, validated_data=input_data)
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
        self.check_field.check_user_permission(user=user, user_permission_name='DeleteTruck')
        # check for required field should be in input data .
        self.check_field.check_field(input_data, required_field='truckId')
        truck_obj = self.get_object(truck_id=input_data.get('truckId'))
        truck_obj.delete()
        data = generate_response(keyword='TRUCK_DELETED')
        return Response(data, status=data.get('statusCode'))
