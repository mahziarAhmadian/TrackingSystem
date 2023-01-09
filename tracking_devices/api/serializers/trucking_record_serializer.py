from rest_framework import serializers
from tracking_devices.models import TruckingRecords, Module, Meter, Truck
from .meter_serializer import MeterSerializer
from .module_serializer import ModuleSerializer
from .truck_serializer import TruckSerializer

class TruckRecordSerializer(serializers.ModelSerializer):
    lat = serializers.CharField(allow_blank=True)
    long = serializers.CharField(allow_blank=True)
    consumption = serializers.FloatField()
    information = serializers.JSONField()
    moduleId = serializers.CharField(write_only=True)
    meterId = serializers.CharField(write_only=True)
    truckId = serializers.CharField(write_only=True)
    moduleInfo = serializers.SerializerMethodField(read_only=True)
    meterInfo = serializers.SerializerMethodField(read_only=True)
    truckInfo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TruckingRecords
        fields = (
            'id', 'lat', 'long', 'consumption', 'information', 'create_time', 'moduleId', 'meterId', 'truckId',
            'meterInfo', 'moduleInfo', 'truckInfo')

    def _validate_meter(self, meter_id):
        # get request method
        request_method = self.context.get('request').method
        allowed_method = ['PATCH', 'PUT']
        if request_method in allowed_method:
            return {"error": False, "value": None}

        # check for object with this id is exists or not .
        try:
            module_obj = Meter.objects.get(id=meter_id)
            return {"error": False, "value": module_obj}
        except:
            return {"error": True, "value": 'METER_NOT_EXISTS'}

    def _validate_module(self, module_id):
        # get request method
        request_method = self.context.get('request').method
        allowed_method = ['PATCH', 'PUT']
        if request_method in allowed_method:
            return {"error": False, "value": None}

        # check for object with this id is exists or not .
        try:
            module_obj = Module.objects.get(id=module_id)
            return {"error": False, "value": module_obj}
        except:
            return {"error": True, "value": 'MODULE_NOT_EXISTS'}

    def _validate_truck(self, truck_id):
        # get request method
        request_method = self.context.get('request').method
        allowed_method = ['PATCH', 'PUT']
        if request_method in allowed_method:
            return {"error": False, "value": None}

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
        meterId = attrs.get('meterId', None)
        moduleId = attrs.get('moduleId', None)
        truckId = attrs.get('truckId', None)

        # ---------------------------------------------------------------------------------
        # validate fields
        meter_obj = self._validate_meter(meter_id=meterId)
        module_obj = self._validate_module(module_id=moduleId)
        truck_obj = self._validate_truck(truck_id=truckId)
        print(f"this is truck obj {truck_obj}")
        # -----------------------------------------------------------------------------------
        # check error exist or not
        errors = list()
        if meter_obj.get("error"):
            errors.append(meter_obj.get("value"))
        if module_obj.get("error"):
            errors.append(module_obj.get("value"))
        if truck_obj.get("error"):
            errors.append(truck_obj.get("value"))
        # ---------------------------------------------------------------------------------
        # if error(s) exists, raise validationError
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        # -----------------------------------------------------------------------------------
        # prepare validated data
        validated_data = {
            'lat': attrs.get('lat'),
            'long': attrs.get('long'),
            'consumption': attrs.get('consumption'),
            'information': attrs.get('information'),
            'meter': meter_obj.get('value'),
            'module': module_obj.get('value'),
            'truck': truck_obj.get('value'),
        }
        # ---------------------------------------------------------------------------------

        return validated_data

    def create(self, validated_data):
        lat = validated_data.pop('lat')
        long = validated_data.pop('long')
        consumption = validated_data.pop('consumption')
        information = validated_data.pop('information')
        meter = validated_data.pop('meter')
        module = validated_data.pop('module')
        truck = validated_data.pop('truck')
        truck_records = TruckingRecords.objects.create(lat=lat, long=long, consumption=consumption,
                                                       information=information, meter=meter, module=module, truck=truck)
        return truck_records

    # --------------------------------------------- for get method------------------------------------------------------
    def get_meterInfo(self, truck_record):
        meter = Meter.objects.get(id=truck_record.meter.id)
        result = MeterSerializer(meter).data
        result.pop('moduleInfo')
        return result

    def get_moduleInfo(self, truck_record):
        module = Module.objects.get(id=truck_record.module.id)
        result = ModuleSerializer(module).data
        return result

    def get_truckInfo(self, truck_record):
        truck = Truck.objects.get(id=truck_record.truck.id)
        result = TruckSerializer(truck).data
        result.pop('meterInfo')
        result['driverInfo'] = {
            'Id': result['driverInfo']['Id'],
            'PhoneNumber': result['driverInfo']['PhoneNumber'],
            'userType': result['driverInfo']['userType'],

        }
        result['ownerInfo'] = {
            'Id': result['ownerInfo']['Id'],
            'PhoneNumber': result['ownerInfo']['PhoneNumber'],
            'userType': result['ownerInfo']['userType'],
        }
        return result
