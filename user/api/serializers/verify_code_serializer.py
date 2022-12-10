from rest_framework import serializers
from user.api.utils.validation import is_email, is_phone_number
from user.models import User, VerificationCode
from general.utils.custom_exception import CustomException
from django.utils import timezone
from datetime import timedelta


class VerifyCodeSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    verificationCode = serializers.CharField(required=False, allow_blank=True)
    codeType = serializers.CharField(required=False, allow_blank=True)

    code_type_choices = ['phoneVerification', 'emailVerification']

    def validate(self, attrs):
        '''
        attrs: ordered dict. contains all parameter that client sent to here as a request.
        '''
        # extract expected fields
        now = timezone.now()
        phone_number = attrs.get('phoneNumber', None)
        email = attrs.get('email', None)
        code_type = attrs.get('codeType', None)
        verification_code = attrs.get('verificationCode', None)
        # ---------------------------------------------------------------------------------
        if code_type is None:
            raise serializers.ValidationError(['CODE_TYPE_REQUIRED'])
        if code_type not in self.code_type_choices:
            raise serializers.ValidationError(['INVALID_CODE_TYPE'])
        if verification_code is None:
            raise serializers.ValidationError(['VERIFICATION_CODE_REQUIRED'])
        # ----------------------------------------------------------------------------------
        if code_type == "phoneVerification":
            if phone_number is None:
                raise serializers.ValidationError(['PHONE_NUMBER_REQUIRED'])
            if not is_phone_number(phone_number):
                raise serializers.ValidationError(['INVALID_PHONE_NUMBER'])
            # ---------------------------------------------------------------------------------
            try:
                user = User.objects.get(phone_number=phone_number)
            except:
                raise CustomException(error_summary='USER_NOT_EXISTS')
            try:
                verification_obj = VerificationCode.objects.get(user=user, type='P')
            except:
                raise CustomException(error_summary='INVALID_OR_EXPIRED_VERIFICATION_CODE')
        # -------------------------------------------------------------------------------------
        elif code_type == "emailVerification":
            if email is None:
                raise serializers.ValidationError(['EMAIL_REQUIRED'])
            if not is_email(email):
                raise serializers.ValidationError(['INVALID_EMAIL_ADDRESS'])
            try:
                user = User.objects.get(email=email)
            except:
                raise CustomException(error_summary='USER_NOT_EXISTS')
            try:
                verification_obj = VerificationCode.objects.get(user=user, type='E')
            except:
                raise CustomException(error_summary='INVALID_OR_EXPIRED_VERIFICATION_CODE')
        # -------------------------------------------------------------------------------------
        if verification_obj.expired_at < now:
            raise CustomException(error_summary='INVALID_OR_EXPIRED_VERIFICATION_CODE')
        if verification_obj.code != verification_code:
            raise CustomException(error_summary='INVALID_OR_EXPIRED_VERIFICATION_CODE')
        # --------------------------------------------------------------------------------------
        if code_type == "phoneVerification":
            user.phone_number_is_valid = True
        elif code_type == "emailVerification":
            user.email_is_valid = True
        user.save()
        verification_obj.expired_at = now - timedelta(minutes=60)
        verification_obj.save()
        return {}
