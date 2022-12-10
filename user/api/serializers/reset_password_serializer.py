from rest_framework import serializers
from user.api.utils.validation import is_email, is_phone_number
from django.utils import timezone
from user.models import User, VerificationCode
from general.utils.custom_exception import CustomException
from datetime import timedelta


class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    newPassword = serializers.CharField(required=False, allow_blank=True)
    oneTimePassword = serializers.CharField(required=False, allow_blank=True)

    def _validate_username(self, username):
        if username is None:
            return {"error": True, "value": "USERNAME_REQUIRED"}
        if is_email(username):
            return {"error": False, "value": username, "type": "email"}
        if is_phone_number(username):
            return {"error": False, "value": username, "type": "phone"}
        return {"error": True, "value": "INVALID_USERNAME"}

    def _validate_password(self, password):
        if password is None:
            return {"error": True, "value": 'PASSWORD_REQUIRED'}
        if len(password) < 6:
            return {"error": True, "value": 'SHORT_LENGTH_PASSWORD'}
        return {"error": False, "value": password}

    def _validate_one_time_password(self, one_time_password):
        if one_time_password is None:
            return {"error": True, "value": "ONE_TIME_PASSWORD_REQUIRED"}
        return {"error": False, "value": one_time_password}

    def validate(self, attrs):
        '''
        attrs: ordered dict. contains all parameter that client sent to here as a request.
        '''
        now = timezone.now()
        # extract expected fields
        username = attrs.get('username', None)
        new_password = attrs.get('newPassword', None)
        one_time_password = attrs.get('oneTimePassword', None)
        # ----------------------------------------------------------------------------------------
        username = self._validate_username(username=username)
        new_password = self._validate_password(password=new_password)
        one_time_password = self._validate_one_time_password(one_time_password=one_time_password)
        # -----------------------------------------------------------------------------------------
        # check that error exists or not
        errors = list()
        if username.get('error'):
            errors.append(username.get('value'))
        if new_password.get('error'):
            errors.append(new_password.get('value'))
        if one_time_password.get('error'):
            errors.append(one_time_password.get('value'))
        # -----------------------------------------------------------------------------------
        # if error(s) exists, raise validationError
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        # ------------------------------------------------------------------------------------
        if username.get('type') == 'email':
            try:
                user = User.objects.get(email=username.get('value'))
            except:
                user = None
        elif username.get('type') == 'phone':
            try:
                user = User.objects.get(phone_number=username.get('value'))
            except:
                user = None
        # ------------------------------------------------------------------------------------
        if user is None:
            raise CustomException(error_summary='USER_NOT_EXISTS')
        # -----------------------------------------------------------------------------------
        if user.blocked:
            raise CustomException(error_summary='USER_IS_BLOCKED')
        # -----------------------------------------------------------------------------------
        error_message = None
        try:
            verification_obj = VerificationCode.objects.get(user=user, type='RST')
            print(verification_obj.code != one_time_password.get('value'))
            print(verification_obj.expired_at)
            print(now)
            if verification_obj.expired_at < now or verification_obj.code != one_time_password.get('value'):
                print("invalid @$@$@@$")
                error_message = 'INVALID_OR_EXPIRED_ONE_TIME_PASSWORD'
        except:
            print("exception@#@#@#")
            error_message = 'INVALID_OR_EXPIRED_ONE_TIME_PASSWORD'
        if error_message is not None:
            raise CustomException(error_summary=error_message)
        # -----------------------------------------------------------------------------------
        verification_obj.expired_at = now - timedelta(minutes=60)
        verification_obj.save()
        # ----------------------------------------------------------------------------------
        user.set_password(new_password.get('value'))
        user.save()
        return {}
