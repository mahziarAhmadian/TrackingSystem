from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.serializers.project_serializer import ProjectSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from user.models import Project
from ..utils import check_field, invalid_error, paginator


class ProjectView(APIView):
    serializer_class = ProjectSerializer
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()
    pagination_class = paginator.CustomPaginator

    def get_object(self, project_id=None):
        if project_id is not None:
            try:
                project_obj = Project.objects.get(id=project_id)
            except:
                errors = []
                extra_fields = {
                    'errorList': errors,
                }
                raise CustomException(error_summary='PROJECT_NOT_EXISTS', extra_fields=extra_fields)
            return project_obj
        else:
            projects = Project.objects.all()
            return projects

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new project .
        required_type_english_name = ['system_administrator', 'municipal_employer']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new project to system .
        self.check_field.check_user_permission(user=user, user_permission_name='AddProject')
        # check for required field should be in input data .
        required_fields = ['englishName', 'persianName', 'image', 'location', 'locationRange', 'startedFrom',
                           'deadline', 'contractNumber', 'contractInformation', 'information', 'owner']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        if input_data.get('owner') is not None:
            user_obj = self.check_field.check_user_exist(user_id=input_data.get('owner'))
            owner = user_obj
        else:
            owner = input_data.get('owner')
        input_data['employer'] = user.id
        serializer = self.serializer_class(data=input_data)
        if serializer.is_valid():
            serializer.save(employer=user, owner=owner)
            data = generate_response(keyword='PROJECT_CREATED')
            return Response(data, status=data.get('statusCode'))
        else:
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)

    def put(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new project .
        required_type_english_name = ['system_administrator', 'municipal_employer']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new project to system .
        self.check_field.check_user_permission(user=user, user_permission_name='EditProject')
        # check for required field should be in input data .
        required_fields = ['projectId', 'englishName', 'persianName', 'image', 'location', 'locationRange',
                           'startedFrom', 'deadline', 'contractNumber', 'contractInformation', 'information', 'owner',
                           'employer']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        project_obj = self.get_object(project_id=input_data.get('projectId'))
        if input_data.get('employer') is None:
            input_data['employer'] = user.id
        else:
            user_obj = self.check_field.check_user_exist(user_id=input_data.get('employer'))
            input_data['employer'] = user_obj.id
        if input_data.get('owner') is None:
            input_data['owner'] = input_data.get('owner')
        else:
            owner_obj = self.check_field.check_user_exist(user_id=input_data.get('owner'))
            input_data['owner'] = owner_obj.id
        serializer = self.serializer_class(project_obj, data=input_data)
        if serializer.is_valid():
            serializer.save()
            data = generate_response(keyword='PROJECT_UPDATED')
            return Response(data, status=data.get('statusCode'))
        else:
            print(serializer.errors)
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)

    def patch(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new project .
        required_type_english_name = ['system_administrator', 'municipal_employer']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new project to system .
        self.check_field.check_user_permission(user=user, user_permission_name='EditProject')
        # check for required field should be in input data .

        self.check_field.check_field(input_data=input_data, required_field='projectId')
        project_obj = self.get_object(project_id=input_data.get('projectId'))
        if 'employer' not in input_data or input_data.get('employer') is None:
            input_data['employer'] = user.id
        if 'owner' in input_data:
            if input_data.get('owner') is None:
                input_data['owner'] = input_data.get('owner')
            else:
                owner_obj = self.check_field.check_user_exist(user_id=input_data.get('owner'))
                input_data['owner'] = owner_obj.id
        serializer = self.serializer_class(project_obj, data=input_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = generate_response(keyword='PROJECT_UPDATED')
            return Response(data, status=data.get('statusCode'))
        else:
            print(serializer.errors)
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)

    def delete(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user type for create new project .
        required_type_english_name = ['system_administrator', 'municipal_employer']
        self.check_field.check_user_type(user=user, required_type_english_name=required_type_english_name)
        # check user permission for add new project to system .
        self.check_field.check_user_permission(user=user, user_permission_name='DeleteProject')
        # check for required field should be in input data .
        self.check_field.check_field(input_data=input_data, required_field='projectId')
        project_obj = self.get_object(project_id=input_data.get('projectId'))
        project_obj.delete()
        data = generate_response(keyword='PROJECT_DELETED')
        return Response(data, status=data.get('statusCode'))

    def get(self, request, *args, **kwargs):
        input_data = request.data
        required_fields = ['page', 'count']
        self.check_field.check_field(required_fields=required_fields, input_data=input_data)
        projects = self.get_object()
        paginator = self.pagination_class(page=input_data.get('page'), count=input_data.get('count'))
        paginated_data = paginator.pagination_query(query_object=projects, order_by_object='create_time')
        serializer = self.serializer_class(paginated_data, many=True)
        project_info = serializer.data
        data = generate_response(keyword='OPERATION_DONE')
        data['allProjectsCount'] = projects.count()
        data['projectInfo'] = project_info
        return Response(data, status=data.get('statusCode'))
        # return Response({"Message": "Test"})
