from rest_framework import serializers
from user.models import UserImage
from .user_serializer import UserSerializer
from . import TypeSerializer, ProfileSerializer
from authorization.api.seializers.permissions_serializer import PermissionSerializer


class UserImageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    SmImage = serializers.ImageField(source='sm_image', allow_empty_file=True, allow_null=True)
    MdImage = serializers.ImageField(source='sm_image', allow_empty_file=True, allow_null=True)
    LgImage = serializers.ImageField(source='sm_image', allow_empty_file=True, allow_null=True)

    class Meta:
        model = UserImage
        fields = ('id', 'user', 'SmImage', 'MdImage', 'LgImage', 'create_time')
