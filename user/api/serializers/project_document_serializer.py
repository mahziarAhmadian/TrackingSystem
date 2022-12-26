from rest_framework import serializers
from user.models import ProjectDocument
import os


class ProjectDocumentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True)
    type = serializers.CharField(allow_blank=True)
    file = serializers.FileField(allow_null=True, allow_empty_file=True, use_url=True)
    information = serializers.JSONField()

    class Meta:
        model = ProjectDocument
        fields = ('id', 'file', 'title', 'type', 'information', 'project')

    def _file_validator(self, file, input_type):
        file_type = os.path.splitext(file.name)[1]

        # valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
        if file_type.lower() != input_type:
            return {"error": True, "value": 'YOUR_FILE_TYPE_NOT_MATCH_WITH_INPUT_TYPE'}
        return {"error": False, "value": file}

    def _validate_type(self, input_type):
        valid_types = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']

        if input_type not in valid_types:
            return {"error": True, "value": 'YOUR_TYPE_IS_NOT_VALID'}
        return {"error": False, "value": input_type}

    def validate(self, attrs):
        '''
        attrs: ordered dict. contains all parameter that client sent to here as a request.
        '''
        file = attrs.get('file', None)
        type = attrs.get('type', None)
        # ---------------------------------------------------------------------------------
        # validate fields
        type = self._validate_type(input_type=type)
        file = self._file_validator(file=file, input_type=type.get('value'))
        # -----------------------------------------------------------------------------------
        # check error exist or not
        errors = list()
        if type.get("error"):
            errors.append(type.get("value"))
        if file.get("error"):
            errors.append(file.get("value"))
        # ---------------------------------------------------------------------------------
        # if error(s) exists, raise validationError
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        # -----------------------------------------------------------------------------------
        # prepare validated data
        validated_data = {
        }
        # ---------------------------------------------------------------------------------
        return attrs
