from rest_framework import serializers
from user.models import User, UserImage, UserType
from . import TypeSerializer, UserImageSerializer
from authorization.api.seializers.permissions_serializer import PermissionSerializer
from user.api.serializers.user_profile_srializer import UserProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    Id = serializers.UUIDField(source='id', read_only=True)
    PhoneNumber = serializers.CharField(source='phone_number', read_only=True)
    PhoneNumberIsValid = serializers.BooleanField(source='phone_number_is_valid', read_only=True)
    Blocked = serializers.BooleanField(source='blocked', required=False)
    isStaff = serializers.BooleanField(source='is_staff', required=False)
    isActive = serializers.BooleanField(source='is_active', required=False)
    isSuperuser = serializers.BooleanField(source='is_superuser', required=False)
    Notes = serializers.CharField(source='notes', required=False, allow_blank=True)
    permissions = PermissionSerializer(many=True, read_only=True)
    userType = serializers.SerializerMethodField()
    profile = UserProfileSerializer(read_only=True)
    Images = serializers.SerializerMethodField()
    firstName = serializers.CharField(source='first_name', read_only=True)
    lastName = serializers.CharField(source='last_name', read_only=True)

    class Meta:
        model = User
        fields = ('Id', 'PhoneNumber', 'PhoneNumberIsValid', 'Blocked', 'isStaff', 'isActive', 'isSuperuser',
                  'Notes', 'permissions', 'userType', 'profile', 'Images', 'firstName', 'lastName')

    def get_Images(self, user):
        images = UserImage.objects.filter(user=user.id)
        return UserImageSerializer(images, many=True).data

    def get_userType(self, user):
        type_object = user.type
        return TypeSerializer(type_object).data
