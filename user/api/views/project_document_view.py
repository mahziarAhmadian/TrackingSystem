from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.serializers.project_document_serializer import ProjectDocumentSerializer
from general.utils import generate_response
from user.models import ProjectDocument
from ..utils import check_field, invalid_error
from .project_view import ProjectView
from general.utils.custom_exception import CustomException
from general.utils.delete_file import DeleteFile


class ProjectDocumentView(APIView):
    # TODO fix with front for file field , if file field null should be sent res with row , if file field not null
    #  should send with form-data.
    serializer_class = ProjectDocumentSerializer
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()
    project = ProjectView()
    delete_file = DeleteFile()

    def get_queryset(self, **kwargs):
        if 'id' in kwargs:
            try:
                doc = ProjectDocument.objects.get(id=kwargs['id'])
                return doc
            except:
                errors = []
                extra_fields = {
                    'errorList': errors,
                }
                raise CustomException(error_summary='PROJECT_DOCUMENT_NOT_EXISTS', extra_fields=extra_fields)
        else:
            filters = {k: v for k, v in kwargs.items()}
            try:
                documents = ProjectDocument.objects.filter(**filters)
            except:
                documents = []
            return documents

    def post(self, request, *args, **kwargs):
        # input_data = {k: v for k, v in request.data.items()}
        input_data = request.data
        user = request.user
        # check user type for create new project .
        required_type_english_name = ['system_administrator', 'municipal_employer']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new project to system .
        self.check_field.check_user_permission(user=user, user_permission_name='AddProject')
        # check for required field should be in input data .
        required_fields = ['file', 'title', 'type', 'link', 'information', 'projectId']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        project_obj = self.project.get_object(project_id=input_data.get('projectId'))
        input_data['project'] = project_obj.id
        serializer = self.serializer_class(data=input_data)
        if serializer.is_valid():
            serializer.save()
            data = generate_response(keyword='PROJECT_DOCUMENT_CREATED')
            return Response(data, status=data.get('statusCode'))
        else:
            print(serializer.errors)
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)

    def get(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new project .
        required_type_english_name = ['system_administrator', 'municipal_employer']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new project to system .
        self.check_field.check_user_permission(user=user, user_permission_name='GetProjectDocuments')
        # check for required field should be in input data .
        required_fields = ['projectId']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        project_obj = self.project.get_object(project_id=input_data.get('projectId'))
        docs = self.get_queryset(project=project_obj.id)
        serializer = self.serializer_class(docs, many=True)
        documents = serializer.data
        data = generate_response(keyword='OPERATION_DONE')
        data['allProjectsDocumentsCount'] = docs.count()
        data['projectDocuments'] = documents
        return Response(data, status=data.get('statusCode'))

    def delete(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user permission for delete  project document from system .
        self.check_field.check_user_permission(user=user, user_permission_name='DeleteProjectDocument')
        # check for required field should be in input data .
        self.check_field.check_field(input_data=input_data, required_field='projectDocumentId')
        project_document_obj = self.get_queryset(id=input_data.get('projectDocumentId'))
        try:
            document_file_path = project_document_obj.file.path
            self.delete_file.delete(file_path=document_file_path)
        except:
            pass
        project_document_obj.delete()
        data = generate_response(keyword='PROJECT_DOCUMENT_DELETED')
        return Response(data, status=data.get('statusCode'))
