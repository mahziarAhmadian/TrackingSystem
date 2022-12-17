from rest_framework import serializers
from user.models import User, UserProfile
from . import TypeSerializer, UserImageSerializer
from authorization.api.seializers.permissions_serializer import PermissionSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    Email = serializers.CharField(source='email', allow_null=True, allow_blank=True)
    FirstName = serializers.CharField(source='first_name', allow_null=True, allow_blank=True)
    LastName = serializers.CharField(source='last_name', allow_null=True, allow_blank=True)
    ZipCode = serializers.CharField(source='zip_code', allow_null=True, allow_blank=True)
    NationalId = serializers.CharField(source='national_id', allow_null=True, allow_blank=True)
    Information = serializers.JSONField(source='information', allow_null=True)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'Email', 'email_is_verified', 'FirstName', 'LastName', 'ZipCode', 'NationalId', 'Information',
            'create_time',)
