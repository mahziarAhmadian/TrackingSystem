from rest_framework import serializers
from tracking_devices.models import Meter, Module
from tracking_devices.api.serializers.module_serializer import ModuleSerializer


class MeterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True, required=True)
    serialNumber = serializers.CharField(source='serial_number', required=True)
    information = serializers.JSONField()
    # module = serializers.UUIDField(required=True)
    moduleInfo = ModuleSerializer(read_only=True)

    class Meta:
        model = Meter
        fields = ('id', 'name', 'serialNumber', 'information', 'create_time', 'moduleInfo', 'module')

    def _validate_module(self, module_id):
        try:
            module_obj = Module.objects.get(id=module_id)
            return {"error": False, "value": module_obj}
        except:
            return {"error": True, "value": 'MODULE_NOT_EXISTS'}
        # is_exist = Meter.objects.filter(module=module_id)
        # if len(is_exist) == 0:
        #     return {"error": False, "value": module_id}
        # else:
        #     return {"error": True, "value": 'SERIAL_NUMBER_IS_NOT_UNIQUE'}

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
        module = attrs.get('module', None)
        # information = attrs.get('information', None)
        # ---------------------------------------------------------------------------------
        # validate fields
        # name = name
        # information = information
        module = self._validate_module(module_id=module)
        serial_number = self._validate_serial_number(serial_number=serialNumber)

        # -----------------------------------------------------------------------------------
        # check error exist or not
        errors = list()
        if module.get("error"):
            errors.append(module.get("value"))
        if serial_number.get("error"):
            errors.append(serial_number.get("value"))
        # ---------------------------------------------------------------------------------
        # if error(s) exists, raise validationError
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        # -----------------------------------------------------------------------------------
        # prepare validated data
        # validated_data = {
        # }
        # ---------------------------------------------------------------------------------
        return attrs
