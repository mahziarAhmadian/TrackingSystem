from rest_framework.views import APIView
from user.api import serializers as S
from rest_framework.response import Response
from general.utils.handle_exception import CustomException
from general.utils.handle_access_authentication import get_authetication_classes


class RefreshTokenView(APIView):

    authentication_classes = get_authetication_classes(api='refresh_token')
    serializer_class = S.RefreshTokenSerializer

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
        return Response(serializer.validated_data, status=serializer.validated_data.get('statusCode'))
