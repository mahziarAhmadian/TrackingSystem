from rest_framework.views import APIView
from rest_framework.response import Response
from general.utils.handle_access_authentication import get_authetication_classes
from user.api.serializers import SendCodeSerializer
from general.utils.custom_exception import CustomException
from user.api.utils import VerificationSender
from general.utils import generate_error, generate_response


class SendCodeAPI(APIView):

    authentication_classes = get_authetication_classes(api='send-code')
    serializer_class = SendCodeSerializer
    verification_sender = VerificationSender()

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
        user = serializer.validated_data.get('user')
        code_type = serializer.validated_data.get('code_type')
        send_to = serializer.validated_data.get('send_to')
        # ------------------------------------------------------------------------------------------
        phone_verification_code = ""
        email_verification_code = ""
        entrance_code = {'phone': "", 'email': ""}
        reset_password_code = {'phone': "", 'email': ""}
        if code_type == 'entrance':
            v_sender_response = self.verification_sender.send(user=user, code_type=code_type, send_to=send_to)
            phone_results = v_sender_response.get('phoneResult')
            email_results = v_sender_response.get('emailResult')
            entrance_code = {
                'phone': phone_results.get('phone_verification_code') if phone_results is not None else "",
                'email': email_results.get('email_verification_code') if email_results is not None else ""
            }
        elif code_type == 'resetPassword':
            v_sender_response = self.verification_sender.send(user=user, code_type=code_type, send_to=send_to)
            phone_results = v_sender_response.get('phoneResult')
            email_results = v_sender_response.get('emailResult')
            reset_password_code = {
                'phone': phone_results.get('phone_verification_code') if phone_results is not None else "",
                'email': email_results.get('email_verification_code') if email_results is not None else ""
            }
        else:
            v_sender_response = self.verification_sender.send(user=user, code_type=send_to)
            phone_verification_code = v_sender_response.get('phone_verification_code', '')
            email_verification_code = v_sender_response.get('email_verification_code', '')
            if v_sender_response.get('error'):
                extra_fields = {
                    'phoneVerificationCode': phone_verification_code,
                    'emailVerificationCode': email_verification_code
                }
                print(extra_fields)
                raise CustomException(error_summary=v_sender_response.get('summary'), extra_fields=extra_fields)
        # ------------------------------------------------------------------------------
        data = generate_response(keyword='CODE_SENT')
        # must be removed after sending verification code testing!
        data['phoneVerificationCode'] = phone_verification_code
        data['emailVerificationCode'] = email_verification_code
        data['entranceVerificationCode'] = entrance_code
        data['resetPasswordCode'] = reset_password_code
        # --------------------------------------------------------------------------------
        return Response(data, status=data.get('status_code'))
