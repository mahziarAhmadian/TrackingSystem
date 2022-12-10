from rest_framework.views import APIView
from rest_framework.response import Response
from user.api import serializers as S
from general.utils.handle_exception import CustomException
from general.utils.handle_access_authentication import get_authetication_classes


class LoginView(APIView):

    authentication_classes = get_authetication_classes(api='login')
    serializer_class = S.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors.get('non_field_errors', None)
            if errors is None:
                errors = []
            extra_fields = {
                'errorList': errors
            }
            raise CustomException(error_summary='INVALID_DATA_RECEIVED', extra_fields=extra_fields)
        return Response(data=serializer.validated_data, status=serializer.validated_data.get('statusCode'))
