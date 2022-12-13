from rest_framework import serializers
from user.models import UserType


class TypeSerializer(serializers.ModelSerializer):
    EnglishName = serializers.CharField(source='english_name', required=True)
    PersianName = serializers.CharField(source='persian_name', required=True)
    Information = serializers.JSONField(source='information', required=True)

    class Meta:
        model = UserType
        fields = ('id', 'EnglishName', 'PersianName', 'Information', 'create_time')
