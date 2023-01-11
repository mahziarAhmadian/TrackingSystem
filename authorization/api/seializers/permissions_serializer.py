from rest_framework import serializers
from authorization.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Permission
        fields = ('id', 'title', 'description', 'created_at')
