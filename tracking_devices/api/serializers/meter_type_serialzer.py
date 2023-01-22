from rest_framework import serializers
from tracking_devices.models import MeterType


class MeterTypeSerializer(serializers.ModelSerializer):
    englishName = serializers.CharField(source='english_name', allow_blank=True, required=True)
    persianName = serializers.CharField(source='persian_name', allow_blank=True, required=True)

    class Meta:
        model = MeterType
        fields = ('id', 'englishName', 'persianName',)
