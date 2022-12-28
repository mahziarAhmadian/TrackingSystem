from rest_framework.views import APIView
from rest_framework.response import Response
from tracking_devices.api.serializers.meter_serializer import MeterSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from tracking_devices.models import Meter
from general.utils import check_field, invalid_error, paginator
from .module_view import ModuleView


class MeterView(APIView):
    serializer_class = MeterSerializer
    pagination_class = paginator.CustomPaginator
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()

    def get_object(self, module_id, filters=None):
        if module_id is None:
            filters = {k: v for k, v in filters.items() if v is not None}
            module_objects = Meter.objects.filter(**filters)
            return module_objects
        else:
            try:
                module_object = Meter.objects.get(id=module_id)
            except:
                errors = []
                extra_fields = {
                    'errorList': errors
                }
                raise CustomException(error_summary='METER_NOT_EXISTS', extra_fields=extra_fields)
            return module_object

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new module .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='AddMeter')
        # check for required field should be in input data .
        required_fields = ['name', 'serialNumber', 'information', 'moduleId']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        input_data['module'] = input_data.get('moduleId')
        serializer = self.serializer_class(data=input_data, context={'request': request})
        if not serializer.is_valid():
            print(serializer.errors)
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)
        serializer.save()
        data = generate_response(keyword='Module_ADDED')
        return Response(data=data, status=data.get('statusCode'))
