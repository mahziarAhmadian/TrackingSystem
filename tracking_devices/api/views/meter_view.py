from rest_framework.views import APIView
from rest_framework.response import Response
from tracking_devices.api.serializers.meter_serializer import MeterSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from tracking_devices.models import Meter
from general.utils import check_field, invalid_error, paginator


class MeterView(APIView):
    serializer_class = MeterSerializer
    pagination_class = paginator.CustomPaginator
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()

    def get_object(self, meter_id, filters=None):
        if meter_id is None:
            filters = {k: v for k, v in filters.items() if v is not None}
            meter_objects = Meter.objects.filter(**filters)
            return meter_objects
        else:
            try:
                meter_objects = Meter.objects.get(id=meter_id)
            except:
                errors = []
                extra_fields = {
                    'errorList': errors
                }
                raise CustomException(error_summary='METER_NOT_EXISTS', extra_fields=extra_fields)
            return meter_objects

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='AddMeter')
        # check for required field should be in input data .
        required_fields = ['name', 'serialNumber', 'information', 'moduleId', 'typeId']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        serializer = self.serializer_class(data=input_data, context={'request': request})
        if not serializer.is_valid():
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)
        serializer.save()
        data = generate_response(keyword='Module_ADDED')
        return Response(data=data, status=data.get('statusCode'))

    def get(self, request, *args, **kwargs):
        # input_data = request.data
        input_data = request.GET
        user = request.user
        data = generate_response(keyword='OPERATION_DONE')
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='GetMeter')
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
            meter_obj = self.get_object(meter_id=None, filters={})
            pagination = self.pagination_class(page=int(input_data.get('page')), count=int(input_data.get('count')))
            module_pagination = pagination.pagination_query(query_object=meter_obj, order_by_object='create_time')
            meter_info = self.serializer_class(module_pagination, many=True).data
            data['allMeterCount'] = meter_obj.count()
        else:
            # check for required field should be in input data .
            self.check_field.check_field(input_data, required_field='meterId')
            meter_obj = self.get_object(meter_id=input_data.get('meterId'))
            meter_info = self.serializer_class(meter_obj).data
        data['meterInfo'] = meter_info
        return Response(data, status=data.get('statusCode'))

    def patch(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='EditMeter')
        # check for required field should be in input data .
        self.check_field.check_field(input_data, required_field='meterId')
        meter_obj = self.get_object(meter_id=input_data.get('meterId'))
        serializer = self.serializer_class(meter_obj, data=input_data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.update(meter_obj, **input_data)
            data = generate_response(keyword='METER_UPDATED')
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
        self.check_field.check_user_permission(user=user, user_permission_name='DeleteMeter')
        # check for required field should be in input data .
        self.check_field.check_field(input_data, required_field='meterId')
        meter_obj = self.get_object(meter_id=input_data.get('meterId'))
        meter_obj.delete()
        data = generate_response(keyword='METER_DELETED')
        return Response(data, status=data.get('statusCode'))
