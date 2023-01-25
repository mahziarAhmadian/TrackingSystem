from rest_framework.views import APIView
from general.utils import check_field, invalid_error, paginator
from rest_framework.response import Response
from tracking_devices.models import Truck, TruckingRecords, TruckMeterSite
from django.utils import timezone
from django.db.models import Sum
from general.utils import generate_response


class ConsumptionReportView(APIView):
    # serializer_class = MeterSiteSerializer
    pagination_class = paginator.CustomPaginator
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()

    def get(self, request, *args, **kwargs):
        # input_data = request.data
        input_data = request.GET
        user = request.user
        result_dict = {}

        # function for calculate all consumption
        def calculate(trucking_records):
            # sum of day record
            for truck_record in trucking_records:
                truck_id = truck_record.truck.id
                if truck_id not in result_dict:
                    trucking_records_consumptions = trucking_records.filter(truck=truck_id).aggregate(
                        Sum('consumption'))
                    truck_meter_site_consumptions = TruckMeterSite.objects.filter(
                        truck=truck_id, create_time__icontains=str(
                            timezone.now().date())).aggregate(Sum('consumption'))
                    result_dict[f'{truck_id}'] = {
                        'truckName': truck_record.truck.name,
                        'totalTruckConsumptions': trucking_records_consumptions['consumption__sum'],
                        'totalTruckMeterSiteConsumptions': truck_meter_site_consumptions['consumption__sum'],
                        'truckEmployerInfo': {
                            'id': truck_record.truck.owner.id,
                            'phone_number': truck_record.truck.owner.phone_number,
                            'type': truck_record.truck.owner.type.english_name,
                        }
                    }

        # check user type .
        user_type = user.type.english_name
        if user_type == 'system_administrator':
            """
            return all meter_site and truck consumption + employer information.
            """
            # this day truck_records
            trucking_records = TruckingRecords.objects.filter(
                create_time__icontains=str(timezone.now().date()))
            calculate(trucking_records=trucking_records)
        if user_type == 'employer':
            """
            return all truck consumption is for login user only.
            """
            # this day truck_records
            trucking_records = TruckingRecords.objects.filter(
                truck__owner=user.id, create_time__icontains=str(timezone.now().date()))
            calculate(trucking_records=trucking_records)
        data = generate_response(keyword='OPERATION_DONE')
        data['totalConsumption'] = result_dict
        return Response(data, status=data.get('statusCode'))
