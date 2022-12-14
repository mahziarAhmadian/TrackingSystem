from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.serializers.user_type_serializer import TypeSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response
from user.models import UserType
from ..utils import check_field, invalid_error, paginator


class UserTypeView(APIView):
    serializer_class = TypeSerializer
    check_field = check_field.CheckField()
    invalid_error = invalid_error.InvalidError()
    pagination_class = paginator.CustomPaginator

    def get_object(self, type_id=None):
        if type_id is None:
            types = UserType.objects.all()
            return types
        try:
            type = UserType.objects.get(id=type_id)
        except:
            errors = []
            extra_fields = {
                'errorList': errors
            }
            raise CustomException(error_summary='TYPE_NOT_EXISTS', extra_fields=extra_fields)
        return type

    def post(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user permission for add new type to system .
        self.check_field.check_user_permission(user=user, user_permission_name='AddType')
        # check for required field should be in input data .
        required_fields = ['EnglishName', 'PersianName', 'Information']
        self.check_field.check_field(input_data=input_data, required_fields=required_fields)
        serializer = self.serializer_class(data=input_data)
        if serializer.is_valid():
            serializer.save()
            data = generate_response(keyword='TYPE_CREATED')
            return Response(data, status=data.get('statusCode'))
        else:
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)

    def get(self, request, *args, **kwargs):
        input_data = request.data
        required_fields = ['page', 'count']
        self.check_field.check_field(required_fields=required_fields, input_data=input_data)
        paginator = self.pagination_class(page=input_data.get('page'), count=input_data.get('count'))
        paginated_data = paginator.pagination_query(query_object=self.get_object(), order_by_object='create_time')
        serializer = self.serializer_class(paginated_data, many=True)
        type_info = serializer.data
        data = generate_response(keyword='OPERATION_DONE')
        data['typeInfo'] = type_info
        return Response(data, status=data.get('statusCode'))

    def patch(self, request, *args, **kwargs):
        input_data = request.data
        user = request.user
        # check user permission for add new type to system .
        self.check_field.check_user_permission(user=user, user_permission_name='EditType')
        # check for required field should be in input data .
        self.check_field.check_field(input_data=input_data, required_field='Id')
        type_object = self.get_object(type_id=input_data['Id'])
        serializer = self.serializer_class(type_object, data=input_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = generate_response(keyword='TYPE_UPDATED')
            return Response(data, status=data.get('statusCode'))
        else:
            self.invalid_error.invalid_serializer(serializer_error=serializer.errors)

    def delete(self, request, *args, **kwargs):
        input_data = request.data
        self.check_field.check_user_permission(user=request.user, user_permission_name='DeleteType')
        self.check_field.check_field(input_data=input_data, required_field='Id')
        type_object = self.get_object(type_id=input_data.get('Id'))
        type_object.delete()
        data = generate_response(keyword='TYPE_DELETED')
        return Response(data, status=data.get('statusCode'))

