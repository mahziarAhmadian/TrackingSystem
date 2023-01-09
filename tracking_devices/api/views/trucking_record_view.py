from rest_framework.views import APIView
from rest_framework.response import Response
from tracking_devices.api.serializers.trucking_record_serializer import TruckRecordSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from tracking_devices.models import TruckingRecords
from general.utils import check_field, invalid_error, paginator


class TruckRecordView(APIView):
    serializer_class = TruckRecordSerializer
    pagination_class = paginator.CustomPaginator
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()

    def get_object(self, truck_record_id=None, filters=None):
        if truck_record_id is None:
            filters = {k: v for k, v in filters.items() if v is not None}
            truck_record_objects = TruckingRecords.objects.filter(**filters)
            return truck_record_objects
        else:
            try:
                truck_record_objects = TruckingRecords.objects.get(id=truck_record_id)
            except:
                errors = []
                extra_fields = {
                    'errorList': errors
                }
                raise CustomException(error_summary='TRUCK_RECORD_NOT_EXISTS', extra_fields=extra_fields)
            return truck_record_objects

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='AddTruckRecord')
        # check for required field should be in input data .
        required_fields = ['lat', 'long', 'consumption', 'information', 'moduleId', 'meterId', 'truckId', ]
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        serializer = self.serializer_class(data=input_data, context={'request': request})
        if not serializer.is_valid():
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)
        serializer.save()
        data = generate_response(keyword='TRUCK_ADDED')
        return Response(data=data, status=data.get('statusCode'))

    def get(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        data = generate_response(keyword='OPERATION_DONE')
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='GetTruckRecord')
        # check method type for get_one or get_all .
        method_type = self.check_field.method_type_check(input_data=input_data)
        if method_type == 'All':
            required_fields = ['page', 'count', 'lat', 'long', 'consumption', 'module', 'meter', 'truck']
            # check for required fields should be in input data .
            self.check_field.check_field(input_data, required_fields=required_fields)
            # filters for get_all
            filters = {
                'lat__icontains': input_data.get('lat'),
                'long__icontains': input_data.get('long'),
                'consumption': input_data.get('consumption'),
                'module': input_data.get('module'),
                'meter': input_data.get('meter'),
                'truck': input_data.get('truck'),
            }
            truck_record_objects = self.get_object(filters=filters)
            pagination = self.pagination_class(page=input_data.get('page'), count=input_data.get('count'))
            truck_record_pagination = pagination.pagination_query(query_object=truck_record_objects,
                                                                  order_by_object='create_time')
            truck_record_info = self.serializer_class(truck_record_pagination, many=True).data
            data['allTruckRecordCount'] = truck_record_objects.count()
        else:
            # check for required field should be in input data .
            self.check_field.check_field(input_data, required_field='truckRecordId')
            truck_record_obj = self.get_object(truck_record_id=input_data.get('truckRecordId'))
            truck_record_info = self.serializer_class(truck_record_obj).data
        data['truckRecordInfo'] = truck_record_info
        return Response(data, status=data.get('statusCode'))

    def delete(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='DeleteTruckRecord')
        # check for required field should be in input data .
        self.check_field.check_field(input_data, required_field='truckRecordId')
        truck_record_obj = self.get_object(truck_record_id=input_data.get('truckRecordId'))
        truck_record_obj.delete()
        data = generate_response(keyword='TRUCK_RECORD_DELETED')
        return Response(data, status=data.get('statusCode'))

    def put(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='EditTruckRecord')
        # check for required field should be in input data .
        required_fields = ['truckRecordId', 'lat', 'long', 'consumption']
        self.check_field.check_field(input_data, required_fields=required_fields)
        truck_record_obj = self.get_object(truck_record_id=input_data.get('truckRecordId'))
        serializer = self.serializer_class(truck_record_obj, data=input_data, context={'request': request},
                                           partial=True)

        if serializer.is_valid():
            serializer.update(instance=truck_record_obj, validated_data=input_data)
            data = generate_response(keyword='TRUCK_RECORD_UPDATED')
            return Response(data, status=data.get('statusCode'))
        else:
            self.invalid_error.invalid_serializer(serializer.errors)
