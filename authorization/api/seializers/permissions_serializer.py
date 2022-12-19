from rest_framework import serializers
from authorization.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'title', 'description', 'created_at')
