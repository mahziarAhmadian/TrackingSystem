from rest_framework import serializers
from tracking_devices.models import Truck, Meter
from .meter_serializer import MeterSerializer
from user.api.serializers.user_serializer import UserSerializer
from user.models import User


class TruckSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True, required=True)
    numberPlate = serializers.CharField(source='number_plate', required=True)
    model = serializers.IntegerField()
    information = serializers.JSONField()
    meterId = serializers.CharField(write_only=True)
    driverId = serializers.CharField(write_only=True)
    ownerId = serializers.CharField(write_only=True)
    meterInfo = serializers.SerializerMethodField(read_only=True)
    driverInfo = serializers.SerializerMethodField(read_only=True)
    ownerInfo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Truck
        fields = ('id', 'name', 'numberPlate', 'model', 'information', 'create_time', 'meterId', 'driverId', 'ownerId',
                  'meterInfo', 'driverInfo', 'ownerInfo')

    def _validate_number_plate(self, number_plate):
        # # get request method
        # request_method = self.context.get('request').method
        # allowed_method = ['PATCH']
        # if request_method in allowed_method:
        #     return {"error": False, "value": meter_id}
        try:
            truck = Truck.objects.get(number_plate=number_plate)
            return {"error": True, "value": 'NUMBER_PLATE_EXISTS'}
        except:
            return {"error": False, "value": number_plate}

    def _validate_meter(self, meter_id):
        # get request method
        request_method = self.context.get('request').method
        allowed_method = ['PATCH', 'PUT']
        if request_method in allowed_method:
            return {"error": False, "value": None}

        # check for object with this id is exists or not .
        try:
            truck = Truck.objects.get(meter__id=meter_id)
            return {"error": True, "value": 'METER_EXISTS'}
        except:
            pass
        try:
            meter_obj = Meter.objects.get(id=meter_id)
            print(f"this is meter_obj : {meter_obj}")
            if meter_obj.meter_type.english_name != 'Truck':
                return {"error": True, "value": 'METER_TYPE_NOT_VALID'}
            return {"error": False, "value": meter_obj}
        except:
            return {"error": True, "value": 'METER_NOT_EXISTS'}

    def _validate_driver(self, driver_id):
        # get request method
        request_method = self.context.get('request').method
        allowed_method = ['PATCH', 'PUT']
        if request_method in allowed_method:
            return {"error": False, "value": None}

        # check for object with this id is exists or not .
        try:
            truck = Truck.objects.get(driver__id=driver_id)
            return {"error": True, "value": 'DRIVER_EXISTS'}
        except:
            pass

        try:
            driver_obj = User.objects.get(id=driver_id)
            return {"error": False, "value": driver_obj}
        except:
            return {"error": True, "value": 'USER_NOT_EXISTS'}

    def _validate_owner(self, owner_id):
        # get request method
        request_method = self.context.get('request').method
        allowed_method = ['PATCH', 'PUT']
        if request_method in allowed_method:
            return {"error": False, "value": None}

        try:
            owner_obj = User.objects.get(id=owner_id)
            return {"error": False, "value": owner_obj}
        except:
            return {"error": True, "value": 'USER_NOT_EXISTS'}

    def validate(self, attrs):
        '''
        attrs: ordered dict. contains all parameter that client sent to here as a request.
        '''

        # extract expected fields
        number_plate = attrs.get('number_plate', None)
        meterId = attrs.get('meterId', None)
        driverId = attrs.get('driverId', None)
        ownerId = attrs.get('ownerId', None)

        # ---------------------------------------------------------------------------------
        # validate fields
        number_plate = self._validate_number_plate(number_plate)
        meter_obj = self._validate_meter(meter_id=meterId)
        driver_obj = self._validate_driver(driver_id=driverId)
        owner_obj = self._validate_owner(owner_id=ownerId)

        # -----------------------------------------------------------------------------------
        # check error exist or not
        errors = list()
        if number_plate.get("error"):
            errors.append(number_plate.get("value"))
        if meter_obj.get("error"):
            errors.append(meter_obj.get("value"))
        if driver_obj.get("error"):
            errors.append(driver_obj.get("value"))
        if owner_obj.get("error"):
            errors.append(owner_obj.get("value"))
        # ---------------------------------------------------------------------------------
        # if error(s) exists, raise validationError
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        # -----------------------------------------------------------------------------------
        # prepare validated data
        validated_data = {
            'name': attrs.get('name'),
            'information': attrs.get('information'),
            'model': attrs.get('model'),
            'number_plate': number_plate.get('value'),
            'meter': meter_obj.get('value'),
            'driver': driver_obj.get('value'),
            'owner': owner_obj.get('value'),
        }
        # ---------------------------------------------------------------------------------

        return validated_data

    def create(self, validated_data):
        name = validated_data.pop('name')
        information = validated_data.pop('information')
        number_plate = validated_data.pop('number_plate')
        model = validated_data.pop('model')
        meter = validated_data.pop('meter')
        driver = validated_data.pop('driver')
        owner = validated_data.pop('owner')
        truck = Truck.objects.create(name=name, information=information, number_plate=number_plate, model=model,
                                     meter=meter, driver=driver, owner=owner, **validated_data)
        return truck

    # --------------------------------------------- for get method------------------------------------------------------
    def get_meterInfo(self, truck):
        meter = Meter.objects.get(id=truck.meter.id)
        result = MeterSerializer(meter).data
        return result

    def get_driverInfo(self, truck):
        user = User.objects.get(id=truck.driver.id)
        result = UserSerializer(user).data
        pop_fields = ['permissions', 'Images']
        for field in pop_fields:
            result.pop(field)
        return result

    def get_ownerInfo(self, truck):
        user = User.objects.get(id=truck.owner.id)
        result = UserSerializer(user).data
        pop_fields = ['permissions', 'Images']
        for field in pop_fields:
            result.pop(field)
        return result
