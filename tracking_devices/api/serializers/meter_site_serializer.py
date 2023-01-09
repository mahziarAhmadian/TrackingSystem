from rest_framework import serializers
from tracking_devices.models import MeterSite, Module
from user.api.serializers.user_serializer import UserSerializer
from user.models.user import User


class MeterSiteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True, required=True)
    lat = serializers.FloatField(required=True)
    long = serializers.FloatField(required=True)
    information = serializers.JSONField()
    ownerId = serializers.CharField(write_only=True)
    ownerInfo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MeterSite
        fields = ('id', 'name', 'lat', 'long', 'information', 'create_time', 'ownerId', 'ownerInfo')

    def _validate_owner(self, user_id):
        # get request method
        request_method = self.context.get('request').method
        allowed_method = ['PATCH', 'PUT']
        if request_method in allowed_method:
            return {"error": False, "value": user_id}
        try:
            user_obj = User.objects.get(id=user_id)
            return {"error": False, "value": user_obj}
        except:
            return {"error": True, "value": 'USER_NOT_EXISTS'}

    def validate(self, attrs):
        '''
        attrs: ordered dict. contains all parameter that client sent to here as a request.
        '''

        # extract expected fields
        ownerId = attrs.get('ownerId', None)
        # ---------------------------------------------------------------------------------
        # validate fields

        owner_obj = self._validate_owner(user_id=ownerId)

        # -----------------------------------------------------------------------------------
        # check error exist or not
        errors = list()
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
            'lat': attrs.get('lat'),
            'long': attrs.get('long'),
            'information': attrs.get('information', None),
            'owner': owner_obj.get('value'),
        }
        # ---------------------------------------------------------------------------------

        return validated_data

    def create(self, validated_data):
        name = validated_data.pop('name')
        lat = validated_data.pop('lat')
        long = validated_data.pop('long')
        information = validated_data.pop('information')
        owner = validated_data.pop('owner')
        meter_site = MeterSite.objects.create(name=name, lat=lat, long=long, information=information, owner=owner,
                                              **validated_data)

        return meter_site

    # --------------------------------------------- for get method------------------------------------------------------
    def get_ownerInfo(self, meter_site):
        owner = User.objects.get(id=meter_site.owner.id)
        result = UserSerializer(owner).data
        result = {
            'Id': result['Id'],
            'PhoneNumber': result['PhoneNumber'],
            'userType': result['userType'],
        }
        return result
