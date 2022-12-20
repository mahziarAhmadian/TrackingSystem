from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.serializers.project_document_serializer import ProjectDocumentSerializer
from general.utils import generate_response
from user.models import ProjectDocument
from ..utils import check_field, invalid_error
from .project_view import ProjectView


class ProjectDocumentView(APIView):
    # TODO project_document.link must match with front dev .
    serializer_class = ProjectDocumentSerializer
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()
    project = ProjectView()

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new project .
        required_type_english_name = ['system_administrator', 'municipal_employer']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new project to system .
        self.check_field.check_user_permission(user=user, user_permission_name='AddProject')
        # check for required field should be in input data .
        required_fields = ['title', 'type', 'link', 'information', 'projectId']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        project_obj = self.project.get_object(project_id=input_data.get('projectId'))
        input_data['project'] = project_obj.id
        serializer = self.serializer_class(data=input_data)
        if serializer.is_valid():
            serializer.save()
            data = generate_response(keyword='PROJECT_DOCUMENT_CREATED')
            return Response(data, status=data.get('statusCode'))
        else:
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)
