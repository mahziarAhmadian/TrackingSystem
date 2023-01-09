from rest_framework import serializers
from tracking_devices.models import TruckMeterSite, MeterSite, Truck
from .truck_serializer import TruckSerializer

class TruckMeterSiteSerializer(serializers.ModelSerializer):
    information = serializers.JSONField()
    meterSiteId = serializers.CharField(write_only=True)
    truckId = serializers.CharField(write_only=True)
    truckInfo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TruckMeterSite
        fields = ('id', 'information', 'create_time', 'meterSiteId', 'truckId', 'truckInfo')

    def _validate_meter_site(self, meter_site_id):
        # get request method
        request_method = self.context.get('request').method
        allowed_method = ['PATCH', 'PUT']
        if request_method in allowed_method:
            return {"error": False, "value": meter_site_id}
        try:
            meter_obj = MeterSite.objects.get(id=meter_site_id)
            return {"error": False, "value": meter_obj}
        except:
            return {"error": True, "value": 'METER_SITE_NOT_EXISTS'}

    def _validate_truck(self, truck_id):
        # get request method
        request_method = self.context.get('request').method
        allowed_method = ['PATCH', 'PUT']
        if request_method in allowed_method:
            return {"error": False, "value": truck_id}
        try:
            truck_obj = Truck.objects.get(id=truck_id)
            return {"error": False, "value": truck_obj}
        except:
            return {"error": True, "value": 'TRUCK_NOT_EXISTS'}

    def validate(self, attrs):
        '''
        attrs: ordered dict. contains all parameter that client sent to here as a request.
        '''

        # extract expected fields
        meterSiteId = attrs.get('meterSiteId', None)
        truckId = attrs.get('truckId', None)
        # ---------------------------------------------------------------------------------
        # validate fields

        meter_site_obj = self._validate_meter_site(meter_site_id=meterSiteId)
        truck_obj = self._validate_truck(truck_id=truckId)

        # -----------------------------------------------------------------------------------
        # check error exist or not
        errors = list()
        if meter_site_obj.get("error"):
            errors.append(meter_site_obj.get("value"))
        if truck_obj.get("error"):
            errors.append(truck_obj.get("value"))

        # ---------------------------------------------------------------------------------
        # if error(s) exists, raise validationError
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        # -----------------------------------------------------------------------------------
        # prepare validated data
        validated_data = {
            'information': attrs.get('information', None),
            'meter_site': meter_site_obj.get('value'),
            'truck': truck_obj.get('value'),
        }
        # ---------------------------------------------------------------------------------

        return validated_data

    def create(self, validated_data):

        information = validated_data.pop('information')
        meter_site = validated_data.pop('meter_site')
        truck = validated_data.pop('truck')
        truck_meter_site = TruckMeterSite.objects.create(information=information, meter_site=meter_site, truck=truck,
                                                         **validated_data)

        return truck_meter_site

    # --------------------------------------------- for get method------------------------------------------------------
    def get_truckInfo(self, truck_meter_site):
        truck = Truck.objects.get(id=truck_meter_site.truck.id)
        result = TruckSerializer(truck).data
        result.pop('meterInfo')
        result.pop('driverInfo')
        result.pop('ownerInfo')
        return result
