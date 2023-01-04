from rest_framework.views import APIView
from rest_framework.response import Response
from tracking_devices.api.serializers.trucking_record_serializer import TruckRecordSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from tracking_devices.models import Truck
from general.utils import check_field, invalid_error, paginator


class TruckView(APIView):
    serializer_class = TruckRecordSerializer
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
        self.check_field.check_user_permission(user=user, user_permission_name='AddTruckRecord')
        # check for required field should be in input data .
        required_fields = ['lat', 'long', 'consumption', 'information', 'moduleId', 'meterId', 'truckId', ]
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        serializer = self.serializer_class(data=input_data, context={'request': request})
        if not serializer.is_valid():
            print(serializer.errors)
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)
        serializer.save()
        data = generate_response(keyword='TRUCK_ADDED')
        return Response(data=data, status=data.get('statusCode'))
