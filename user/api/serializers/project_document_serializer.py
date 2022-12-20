from rest_framework import serializers
from user.models import ProjectDocument


class ProjectDocumentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True)
    type = serializers.CharField(allow_blank=True)
    link = serializers.URLField(allow_null=True, allow_blank=True)
    information = serializers.JSONField()

    class Meta:
        model = ProjectDocument
        fields = ('title', 'type', 'link', 'information','project')
