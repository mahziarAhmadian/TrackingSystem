from rest_framework.views import APIView
from rest_framework.response import Response
from tracking_devices.api.serializers.meter_type_serialzer import MeterTypeSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from tracking_devices.models import MeterType
from general.utils import check_field, invalid_error, paginator


class MeterTypeView(APIView):
    serializer_class = MeterTypeSerializer
    pagination_class = paginator.CustomPaginator
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()

    def get_object(self, meter_type_id=None):
        if meter_type_id is None:
            meter_types = MeterType.objects.all()
            return meter_types

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='AddMeterType')
        # check for required field should be in input data .
        required_fields = ['englishName', 'persianName']
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
        self.check_field.check_user_permission(user=user, user_permission_name='GetMeterType')
        meter_types = self.get_object()
        # serialize
        meter_types_info = self.serializer_class(meter_types, many=True).data
        data['meterTypes'] = meter_types_info
        return Response(data, status=data.get('statusCode'))
