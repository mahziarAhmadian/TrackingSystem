from rest_framework import serializers
from tracking_devices.models import Meter, Module, MeterType
from tracking_devices.api.serializers.module_serializer import ModuleSerializer
from tracking_devices.api.serializers.meter_type_serialzer import MeterTypeSerializer


class MeterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True, required=True)
    serialNumber = serializers.CharField(source='serial_number', required=True)
    moduleId = serializers.CharField(write_only=True)
    typeId = serializers.CharField(write_only=True)
    information = serializers.JSONField()
    moduleInfo = serializers.SerializerMethodField(read_only=True)
    meterTypeInfo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Meter
        fields = (
            'id', 'name', 'serialNumber', 'information', 'create_time', 'moduleId', 'typeId', 'moduleInfo',
            'meterTypeInfo')

    def _validate_module(self, module_id):
        # get request method
        request_method = self.context.get('request').method
        allowed_method = ['PATCH']
        if request_method in allowed_method:
            return {"error": False, "value": module_id}
        try:
            module_obj = Module.objects.get(id=module_id)
            return {"error": False, "value": module_obj}
        except:
            return {"error": True, "value": 'MODULE_NOT_EXISTS'}

    def _validate_meter_type(self, type_id):
        # get request method
        request_method = self.context.get('request').method
        allowed_method = ['PATCH', 'PUT']
        if request_method in allowed_method:
            return {"error": False, "value": type_id}
        try:
            type_obj = MeterType.objects.get(id=type_id)
            return {"error": False, "value": type_obj}
        except:
            return {"error": True, "value": 'TYPE_NOT_EXISTS'}

    def _validate_serial_number(self, serial_number):
        # get request method
        request_method = self.context.get('request').method
        allowed_method = ['PUT']
        if request_method in allowed_method:
            return {"error": False, "value": serial_number}
        is_exist = Meter.objects.filter(serial_number=serial_number)
        if len(is_exist) == 0:
            return {"error": False, "value": serial_number}
        else:
            return {"error": True, "value": 'SERIAL_NUMBER_IS_NOT_UNIQUE'}

    def validate(self, attrs):
        '''
        attrs: ordered dict. contains all parameter that client sent to here as a request.
        '''

        # extract expected fields
        # name = attrs.get('name', None)
        serialNumber = attrs.get('serial_number', None)
        moduleId = attrs.get('moduleId', None)
        typeId = attrs.get('typeId', None)
        # information = attrs.get('information', None)
        # ---------------------------------------------------------------------------------
        # validate fields
        # name = name
        # information = information
        module = self._validate_module(module_id=moduleId)
        meter_type = self._validate_meter_type(type_id=typeId)
        serial_number = self._validate_serial_number(serial_number=serialNumber)

        # -----------------------------------------------------------------------------------
        # check error exist or not
        errors = list()
        if module.get("error"):
            errors.append(module.get("value"))
        if meter_type.get("error"):
            errors.append(module.get("value"))
        if serial_number.get("error"):
            errors.append(serial_number.get("value"))
        # ---------------------------------------------------------------------------------
        # if error(s) exists, raise validationError
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        # -----------------------------------------------------------------------------------
        # prepare validated data
        validated_data = {
            # 'first_name': first_name.get('value'),
            # 'last_name': last_name.get('value'),
            'name': attrs.get('name'),
            'serialNumber': serial_number.get('value'),
            'information': attrs.get('information'),
            'module': module.get('value'),
            'meter_type': meter_type.get('value'),
        }
        # ---------------------------------------------------------------------------------

        return validated_data

    def create(self, validated_data):
        name = validated_data.pop('name')
        serialNumber = validated_data.pop('serialNumber')
        module = validated_data.pop('module')
        meter_type = validated_data.pop('meter_type')
        information = validated_data.pop('information')
        meter = Meter.objects.create(name=name, serial_number=serialNumber, module=module, information=information,
                                     meter_type=meter_type, **validated_data)

        return meter

    def update(self, meter, **kwargs):
        if 'information' in kwargs:
            meter.information = kwargs.get('information')
        if 'name' in kwargs:
            meter.name = kwargs.get('name')
        meter.save()
        return meter

    # --------------------------------------function for get method-----------------------------------------------------

    def get_moduleInfo(self, meter):
        module = Module.objects.get(id=meter.module.id)
        result = ModuleSerializer(module).data
        return result

    def get_meterTypeInfo(self, meter):
        meter_type = MeterType.objects.get(id=meter.meter_type.id)
        result = MeterTypeSerializer(meter_type).data
        return result
