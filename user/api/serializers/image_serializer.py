from rest_framework import serializers
from user.models import UserImage


class UserImageSerializer(serializers.ModelSerializer):
    SmImage = serializers.ImageField(source='sm_image', allow_empty_file=True, allow_null=True)
    MdImage = serializers.ImageField(source='md_image', allow_empty_file=True, allow_null=True)
    LgImage = serializers.ImageField(source='lg_image', allow_empty_file=True, allow_null=True)

    class Meta:
        model = UserImage
        fields = ('id', 'user', 'SmImage', 'MdImage', 'LgImage', 'create_time')
