from rest_framework import serializers
from tracking_devices.models import Module


class ModuleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True, required=True)
    serialNumber = serializers.CharField(source='serial_number', required=True)
    information = serializers.JSONField()

    class Meta:
        model = Module
        fields = ('id', 'name', 'serialNumber', 'information', 'create_time')

    def _validate_serial_number(self, serial_number):
        # get request method
        request_method = self.context.get('request').method
        allowed_method = ['PUT']
        if request_method in allowed_method:
            return {"error": False, "value": serial_number}
        is_exist = Module.objects.filter(serial_number=serial_number)
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
        # information = attrs.get('information', None)
        # ---------------------------------------------------------------------------------
        # validate fields
        # name = name
        # information = information
        serial_number = self._validate_serial_number(serial_number=serialNumber)
        # -----------------------------------------------------------------------------------
        # check error exist or not
        errors = list()
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
