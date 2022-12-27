from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.serializers import RegisterSerializer
from general.utils.handle_exception import CustomException
from general.utils import generate_response, generate_error
from general.utils.handle_access_authentication import get_authetication_classes
from user.api.utils import VerificationSender


class RegisterAPI(APIView):
    authentication_classes = get_authetication_classes(api='register')
    serializer_class = RegisterSerializer
    verification_sender = VerificationSender()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            errors = serializer.errors.get('non_field_errors', None)
            if errors is None:
                errors = []
            extra_fields = {
                'errorList': errors
            }
            raise CustomException(error_summary='INVALID_DATA_RECEIVED', extra_fields=extra_fields)
        user = serializer.save()
        data = generate_response(keyword='USER_CREATED')
        v_sender_response = self.verification_sender.send(user=user, code_type='phone')
        if v_sender_response.get('error'):
            error_list = [generate_error(keyword=v_sender_response.get('summary'))]
            data["errorList"] = error_list
        # ------------------------------------------------------------------------------
        # must be removed after sending verification code testing!
        verification_code = v_sender_response.get('phone_verification_code')
        data['verificationCode'] = verification_code
        # -------------------------------------------------------------------------------
        return Response(data=data, status=data.get('statusCode'))
