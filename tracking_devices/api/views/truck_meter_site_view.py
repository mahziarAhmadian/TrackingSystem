from rest_framework.views import APIView
from rest_framework.response import Response
from tracking_devices.api.serializers.truck_meter_site_serializer import TruckMeterSiteSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from tracking_devices.models import TruckMeterSite
from general.utils import check_field, invalid_error, paginator


class TruckMeterSiteView(APIView):
    serializer_class = TruckMeterSiteSerializer
    pagination_class = paginator.CustomPaginator
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()

    def get_object(self, truck_meter_site_id=None, filters=None):
        if truck_meter_site_id is None:
            filters = {k: v for k, v in filters.items() if v is not None}
            truck_meter_site_objects = TruckMeterSite.objects.filter(**filters)
            return truck_meter_site_objects
        else:
            try:
                truck_meter_site_object = TruckMeterSite.objects.get(id=truck_meter_site_id)
            except:
                errors = []
                extra_fields = {
                    'errorList': errors
                }
                raise CustomException(error_summary='TRUCK_METER_NOT_EXISTS', extra_fields=extra_fields)
            return truck_meter_site_object

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='AddTruckMeterSite')
        # check for required field should be in input data .
        required_fields = ['information', 'meterSiteId', 'truckId']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        serializer = self.serializer_class(data=input_data, context={'request': request})
        if not serializer.is_valid():
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)
        serializer.save()
        data = generate_response(keyword='TRUCK_METER_SITE_CREATED')
        return Response(data=data, status=data.get('statusCode'))

    def get(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        data = generate_response(keyword='OPERATION_DONE')
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='GetTruckMeterSite')
        # check method type for get_one or get_all .
        method_type = self.check_field.method_type_check(input_data=input_data)
        if method_type == 'All':
            required_fields = ['page', 'count', 'meterSiteId', 'truckId']
            # check for required fields should be in input data .
            self.check_field.check_field(input_data, required_fields=required_fields)
            # filters for get_all
            filters = {
                'truck__id': input_data.get('truckId'),
                'meter_site__id': input_data.get('meterSiteId'),
            }
            truck_meter_site_obj = self.get_object(filters=filters)
            pagination = self.pagination_class(page=input_data.get('page'), count=input_data.get('count'))
            truck_meter_site_pagination = pagination.pagination_query(query_object=truck_meter_site_obj,
                                                                      order_by_object='create_time')
            truck_meter_site_info = self.serializer_class(truck_meter_site_pagination, many=True).data
            data['allTruckMeterSiteCount'] = truck_meter_site_obj.count()
        else:
            # check for required field should be in input data .
            self.check_field.check_field(input_data, required_field='truckMeterSiteId')
            truck_meter_site_obj = self.get_object(truck_meter_site_id=input_data.get('truckMeterSiteId'))
            truck_meter_site_info = self.serializer_class(truck_meter_site_obj).data
        data['truckMeterSiteInfo'] = truck_meter_site_info
        return Response(data, status=data.get('statusCode'))

    def delete(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='DeleteTruckMeterSite')
        # check for required field should be in input data .
        self.check_field.check_field(input_data, required_field='truckMeterSiteId')
        truck_obj = self.get_object(truck_meter_site_id=input_data.get('truckMeterSiteId'))
        truck_obj.delete()
        data = generate_response(keyword='TRUCK_METER_SITE_DELETED')
        return Response(data, status=data.get('statusCode'))