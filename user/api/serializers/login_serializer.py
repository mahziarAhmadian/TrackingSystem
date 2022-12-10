from ast import keyword
from distutils.log import error
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from user.models.user import User
from core.settings import SIMPLE_JWT
from rest_framework import serializers
from django.contrib.auth import authenticate
from user.api.utils.validation import is_email, is_phone_number
from general.utils.handle_exception import CustomException
from general.utils import generate_response
from user.models import VerificationCode
from django.utils import timezone
from datetime import timedelta


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", {})
        kwargs["style"]["input_type"] = "password"
        kwargs["write_only"] = True,
        kwargs['required'] = False,
        kwargs['allow_blank'] = True
        super().__init__(*args, **kwargs)


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(required=False, allow_blank=True)
    password = PasswordField()
    loginType = serializers.CharField(required=False, allow_blank=True)
    entranceCode = serializers.CharField(required=False, allow_blank=True)

    login_type_choices = ['password', 'code']

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

    def _validate_code(self, code):
        if code is None:
            return {"error": True, "value": "ENTRANCE_CODE_REQUIRED"}
        return {"error": False, "value": code}

    def validate(self, attrs):
        '''
        attrs: ordered dict. contains all parameter that client sent to here as a request.
        '''
        now = timezone.now()
        # extract expected fields
        username = attrs.get('username', None)
        password = attrs.get('password', None)
        entrance_code = attrs.get('entranceCode', None)
        login_type = attrs.get('loginType', None)
        # --------------------------------------------------------------------------------
        # validate fields
        if login_type is None:
            raise serializers.ValidationError(['LOGIN_TYPE_REQUIRED'])
        if login_type not in self.login_type_choices:
            raise serializers.ValidationError(['INVALID_LOGIN_TYPE'])

        username = self._validate_username(username=username)
        if login_type == 'password':
            password = self._validate_password(password=password)
        elif login_type == 'code':
            entrance_code = self._validate_code(code=entrance_code)
        # ---------------------------------------------------------------------------------
        # check that error exists or not
        errors = list()
        if username.get('error'):
            errors.append(username.get('value'))
        try:
            if password.get('error'):
                errors.append(password.get('value'))
        except:
            pass
        try:
            if entrance_code.get('error'):
                errors.append(entrance_code.get('value'))
        except:
            pass
        # -----------------------------------------------------------------------------------
        # if error(s) exists, raise validationError
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        # -----------------------------------------------------------------------------------
        # try to authenticate user
        if login_type == 'password':
            user = authenticate(username=username.get('value'),
                                password=password.get('value'))
        else:
            error_message = None
            try:
                user = User.objects.get(phone_number=username.get('value'))
                try:
                    verification_obj = VerificationCode.objects.get(user=user, type='EN')
                    if verification_obj.expired_at < now or verification_obj.code != entrance_code.get('value'):
                        error_message = 'INVALID_OR_EXPIRED_ENTRANCE_CODE'
                    else:
                        verification_obj.expired_at = now - timedelta(minutes=60)
                        verification_obj.save()
                except:
                    error_message = 'INVALID_OR_EXPIRED_ENTRANCE_CODE'
            except:
                user = None
            if error_message is not None:
                raise CustomException(error_message)
        # -----------------------------------------------------------------------------------
        # authentication failed. user not exists
        if user is None:
            raise CustomException(error_summary='USER_NOT_EXISTS')
        # -----------------------------------------------------------------------------------
        # check forbidden contition
        if user.blocked:
            raise CustomException(error_summary='USER_IS_BLOCKED')

        if username.get('type') == 'email' and not user.email_is_valid:
            raise CustomException(error_summary='EMAIL_SHOULD_BE_VALIDATED')

        if username.get('type') == 'phone' and not user.phone_number_is_valid:
            raise CustomException(error_summary='PHONE_NUMBER_SHOULD_BE_VALIDATED')
        # --------------------------------------------------------------------------------------

        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        if SIMPLE_JWT.get('UPDATE_LAST_LOGIN'):
            update_last_login(None, user)

        data = generate_response(keyword='LOGIN_SUCCESSFUL')
        data['token'] = token
        return data
