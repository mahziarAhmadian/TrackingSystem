from rest_framework.views import APIView
from rest_framework.response import Response
from tracking_devices.api.serializers.meter_site_serializer import MeterSiteSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from tracking_devices.models import Meter, Module, Truck
from user.models.user import User
from general.utils import check_field, invalid_error, paginator


class CounterView(APIView):
    # serializer_class = MeterSiteSerializer
    pagination_class = paginator.CustomPaginator
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()

    def get_object(self, models_name):
        counter_dict = {}
        for name in models_name:
            if name == 'Meter':
                count_all_data = Meter.objects.all().count()
                counter_dict['meterNumber'] = count_all_data
            elif name == 'Module':
                count_all_data = Module.objects.all().count()
                counter_dict['moduleNumber'] = count_all_data
            elif name == 'Truck':
                count_all_data = Truck.objects.all().count()
                counter_dict['truckNumber'] = count_all_data
            elif name == 'user':
                count_all_data_admin = User.objects.filter(type__english_name='system_administrator').count()
                count_all_data = User.objects.filter(type__english_name='BasicUser').count()
                counter_dict['systemAdminNumber'] = count_all_data_admin
                counter_dict['basicNumber'] = count_all_data
        return counter_dict

    def get(self, request, *args, **kwargs):
        # input_data = request.data
        user = request.user
        data = generate_response(keyword='OPERATION_DONE')
        # check user type .
        required_type_english_name = ['system_administrator']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new module to system .
        self.check_field.check_user_permission(user=user, user_permission_name='CountAllData')
        models_name = ['Meter', 'Module', 'Truck', 'user']
        counter = self.get_object(models_name=models_name)
        data = generate_response(keyword='OPERATION_DONE')
        data['allModelNumber'] = counter
        return Response(data=data, status=data.get('statusCode'))
