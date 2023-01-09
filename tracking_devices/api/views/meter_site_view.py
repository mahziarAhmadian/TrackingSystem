from rest_framework.views import APIView
from rest_framework.response import Response
from tracking_devices.api.serializers.meter_site_serializer import MeterSiteSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from tracking_devices.models import MeterSite
from general.utils import check_field, invalid_error, paginator


class MeterSiteView(APIView):
    serializer_class = MeterSiteSerializer
    pagination_class = paginator.CustomPaginator
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()

    def get_object(self, meter_site_id, filters=None):
        if meter_site_id is None:
            filters = {k: v for k, v in filters.items() if v is not None}
            meter_site_objects = MeterSite.objects.filter(**filters)
            return meter_site_objects
        else:
            try:
                meter_site_objects = MeterSite.objects.get(id=meter_site_id)
            except:
                errors = []
                extra_fields = {
                    'errorList': errors
                }
                raise CustomException(error_summary='METER_SITE_NOT_EXISTS', extra_fields=extra_fields)
            return meter_site_objects

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='AddMeterSite')
        # check for required field should be in input data .
        required_fields = ['name', 'lat', 'long', 'information', 'ownerId']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        serializer = self.serializer_class(data=input_data, context={'request': request})
        if not serializer.is_valid():
            print(serializer.errors)
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)
        serializer.save()
        data = generate_response(keyword='METER_SITE_CREATED')
        return Response(data=data, status=data.get('statusCode'))

    def get(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        data = generate_response(keyword='OPERATION_DONE')
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='GetMeterSite')
        # check method type for get_one or get_all .
        method_type = self.check_field.method_type_check(input_data=input_data)
        if method_type == 'All':
            required_fields = ['page', 'count', 'name', 'lat', 'long', 'ownerId']
            # check for required fields should be in input data .
            self.check_field.check_field(input_data, required_fields=required_fields)
            # filters for get_all
            filters = {
                'name__icontains': input_data.get('name'),
                'lat__icontains': input_data.get('lat'),
                'long__icontains': input_data.get('long'),
                'owner': input_data.get('ownerId'),
            }
            meter_site_obj = self.get_object(meter_site_id=None, filters=filters)
            pagination = self.pagination_class(page=input_data.get('page'), count=input_data.get('count'))
            meter_site_pagination = pagination.pagination_query(query_object=meter_site_obj,
                                                                order_by_object='create_time')
            meter_site_info = self.serializer_class(meter_site_pagination, many=True).data
            data['allMeterSiteCount'] = meter_site_obj.count()
        else:
            # check for required field should be in input data .
            self.check_field.check_field(input_data, required_field='meterSiteId')
            meter_site_obj = self.get_object(meter_site_id=input_data.get('meterSiteId'))
            meter_site_info = self.serializer_class(meter_site_obj).data
        data['meterSiteInfo'] = meter_site_info
        return Response(data, status=data.get('statusCode'))

    def delete(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='DeleteMeterSite')
        # check for required field should be in input data .
        self.check_field.check_field(input_data, required_field='meterSiteId')
        meter_obj = self.get_object(meter_site_id=input_data.get('meterSiteId'))
        meter_obj.delete()
        data = generate_response(keyword='METER_SITE_DELETED')
        return Response(data, status=data.get('statusCode'))

    def put(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='EditMeterSite')
        # check for required field should be in input data .
        required_fields = ['meterSiteId', 'name', 'lat', 'long', 'information', ]
        self.check_field.check_field(input_data, required_fields=required_fields)
        meter_site_obj = self.get_object(meter_site_id=input_data.get('meterSiteId'))
        serializer = self.serializer_class(meter_site_obj, data=input_data, context={'request': request},
                                           partial=True)

        if serializer.is_valid():
            serializer.update(instance=meter_site_obj, validated_data=input_data)
            data = generate_response(keyword='METER_SITE_UPDATED')
            return Response(data, status=data.get('statusCode'))
        else:
            self.invalid_error.invalid_serializer(serializer.errors)
