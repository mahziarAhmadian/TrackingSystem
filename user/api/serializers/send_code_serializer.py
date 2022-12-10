from rest_framework import serializers
from user.api.utils.validation import is_email, is_phone_number
from user.models import User
from general.utils.custom_exception import CustomException


class SendCodeSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    codeType = serializers.CharField(required=False, allow_blank=True)

    code_type_choices = ['phoneVerification', 'emailVerification', 'entrance', 'resetPassword']

    def validate(self, attrs):
        '''
        attrs: ordered dict. contains all parameter that client sent to here as a request.
        '''
        # extract expected fields
        phone_number = attrs.get('phoneNumber', None)
        email = attrs.get('email', None)
        code_type = attrs.get('codeType', None)
        send_to = None  # options: email, phone, both
        # ---------------------------------------------------------------------------------
        if code_type is None:
            raise serializers.ValidationError(['CODE_TYPE_REQUIRED'])
        if code_type not in self.code_type_choices:
            raise serializers.ValidationError(['INVALID_CODE_TYPE'])
        # ----------------------------------------------------------------------------------
        if code_type == "phoneVerification":
            if phone_number is None:
                raise serializers.ValidationError(['PHONE_NUMBER_REQUIRED'])
            if not is_phone_number(phone_number):
                raise serializers.ValidationError(['INVALID_PHONE_NUMBER'])
            send_to = 'phone'
        # -------------------------------------------------------------------------------------
        elif code_type == "emailVerification":
            if email is None:
                raise serializers.ValidationError(['EMAIL_REQUIRED'])
            if not is_email(email):
                raise serializers.ValidationError(['INVALID_EMAIL_ADDRESS'])
            send_to = 'email'
        # -------------------------------------------------------------------------------------
        elif code_type == 'entrance' or code_type == 'resetPassword':
            if phone_number is None and email is None:
                raise serializers.ValidationError(['PHONE_NUMBER_OR_EMAIL_REQUIRED'])
            email_is_valid = is_email(email)
            phone_is_valid = is_phone_number(phone_number)
            if not email_is_valid and not phone_is_valid:
                raise serializers.ValidationError(['INVALID_PHONE_NUMBER', 'INVALID_EMAIL_ADDRESS'])
            elif email_is_valid and not phone_is_valid:
                send_to = 'email'
            elif not email_is_valid and phone_is_valid:
                send_to = 'phone'
            else:
                send_to = 'both'
        # -------------------------------------------------------------------------------------
        print(code_type)
        print(phone_number)
        print(email)
        print(send_to)
        if send_to == 'email':
            error_message = None
            try:
                user = User.objects.get(email=email)
                if (code_type == 'entrance' or code_type == 'resetPassword') and not user.email_is_valid:
                    error_message = 'EMAIL_SHOULD_BE_VALIDATED'
            except:
                raise CustomException(error_summary='USER_NOT_EXISTS')
            if error_message is not None:
                raise CustomException(error_message)
        elif send_to == 'phone':
            error_message = None
            try:
                user = User.objects.get(phone_number=phone_number)
                if (code_type == 'entrance' or code_type == 'resetPassword') and not user.phone_number_is_valid:
                    error_message = 'PHONE_NUMBER_SHOULD_BE_VALIDATED'
            except:
                raise CustomException(error_summary='USER_NOT_EXISTS')
            if error_message is not None:
                raise CustomException(error_message)
        else:
            error_message = None
            try:
                user = User.objects.get(phone_number=phone_number, email=email)
                if code_type == 'entrance' or code_type == 'resetPassword':
                    if not user.email_is_valid and not user.phone_number_is_valid:
                        error_message = 'PHONE_NUMBER_AND_EMAIL_SHOULD_BE_VALIDATED'
                    elif user.email_is_valid and not user.phone_number_is_valid:
                        send_to = 'email'
                    elif not user.email_is_valid and user.phone_number_is_valid:
                        send_to = 'phone'
            except:
                raise CustomException(error_summary='USER_NOT_EXISTS')
            if error_message is not None:
                raise CustomException(error_message)
        # --------------------------------------------------------------------------------------
        if user.blocked:
            raise CustomException(error_summary='USER_IS_BLOCKED')
        # --------------------------------------------------------------------------------------
        return {
            'user': user,
            'code_type': code_type,
            'send_to': send_to
        }
