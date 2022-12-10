from gc import get_referents
from rest_framework.views import APIView
from rest_framework.response import Response
from general.utils.handle_access_authentication import get_authetication_classes
from user.api.serializers import VerifyCodeSerializer
from general.utils.custom_exception import CustomException
from general.utils import generate_response


class VerifyCodeAPI(APIView):

    authentication_classes = get_authetication_classes(api='verify-code')
    serializer_class = VerifyCodeSerializer

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
        # -------------------------------------------------------------------------------------------
        data = generate_response(keyword='CODE_VERIFIED')
        return Response(data, status=data.get('statusCode'))
