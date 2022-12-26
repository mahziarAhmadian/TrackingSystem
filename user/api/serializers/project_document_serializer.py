from rest_framework import serializers
from user.models import ProjectDocument


class ProjectDocumentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True)
    type = serializers.CharField(allow_blank=True)
    link = serializers.URLField(allow_null=True, allow_blank=True)
    file = serializers.FileField(allow_null=True, allow_empty_file=True, use_url=True)
    information = serializers.JSONField()

    class Meta:
        model = ProjectDocument
        fields = ('id', 'file', 'title', 'type', 'link', 'information', 'project')
