from rest_framework.views import APIView
from rest_framework.response import Response
from user.api.serializers import ProfileSerializer
from general.utils.custom_exception import CustomException
from user.api.utils import VerificationSender
from general.utils import generate_response


class ProfileAPI(APIView):
    serializer_class = ProfileSerializer
    verification_sender = VerificationSender()

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors.get('non_field_errors', None)
            if errors is None:
                errors = []
            extra_fields = {
                'errorList': errors
            }
            raise CustomException(error_summary='INVALID_DATA_RECEIVED', extra_fields=extra_fields)
        user = serializer.update(user=request.user)
        phone_changed = serializer.validated_data.get('phone_changed')
        email_changed = serializer.validated_data.get('email_changed')
        data = generate_response(keyword='USER_UPDATED')
        data['phoneVerificationCode'] = ''
        data['emailVerificationCode'] = ''
        if phone_changed:
            v_sender_response = self.verification_sender.send(user=user, code_type='phone')
            data['phoneVerificationCode'] = v_sender_response.get('phone_verification_code')
        if email_changed:
            v_sender_response = self.verification_sender.send(user=user, code_type='email', send_to='email')
            data['emailVerificationCode'] = v_sender_response.get('email_verification_code')
        data['phoneNumberChanged'] = phone_changed
        data['emailCahnged'] = email_changed
        user_data = self.serializer_class(user).data
        data['userInfo'] = user_data
        return Response(data, status=data.get('statusCode'))

    def get(self, request, *args, **kwargs):
        user_info = self.serializer_class(request.user).data

        data = generate_response(keyword='OPERATION_DONE')
        data['userInfo'] = user_info
        return Response(data, status=data.get('statusCode'))
