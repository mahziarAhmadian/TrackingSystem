from rest_framework import serializers
from user.api.utils.validation import is_email, is_phone_number, is_national_id
from user.models import User, UserImage, UserType, UserProfile
from general.utils.custom_exception import CustomException
from authorization.models import Permission


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id', 'email', 'email_is_verified', 'first_name', 'last_name', 'zip_code', 'national_id', 'information',
            'create_time',)


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ('id', 'english_name', 'persian_name', 'information', 'create_time')


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'title', 'description', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    Id = serializers.UUIDField(source='id', read_only=True)
    PhoneNumber = serializers.CharField(source='phone_number', read_only=True)
    PhoneNumberIsValid = serializers.BooleanField(source='phone_number_is_valid', read_only=True)
    Blocked = serializers.BooleanField(source='blocked', required=False)
    isStaff = serializers.BooleanField(source='is_staff', required=False)
    isActive = serializers.BooleanField(source='is_active', required=False)
    isSuperuser = serializers.BooleanField(source='is_superuser', required=False)
    Notes = serializers.CharField(source='notes', required=False)
    permissions = PermissionSerializer(many=True, read_only=True)
    type = TypeSerializer(many=True, read_only=True)
    profile = TypeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('Id', 'PhoneNumber', 'PhoneNumberIsValid', 'Blocked', 'isStaff', 'isActive', 'isSuperuser',
                  'Notes', 'permissions', 'type', 'profile')
