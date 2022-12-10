from lib2to3.pgen2 import token
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from core.settings import SIMPLE_JWT
from general.utils.handle_exception import CustomException
from general.utils import generate_response


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=False, allow_blank=True)
    access = serializers.CharField(read_only=True)

    def _validate_refresh(self, refresh):
        if refresh is None:
            return {"error": True, "value": "REFRESH_TOKEN_REQUIRED"}
        if not isinstance(refresh, str):
            return {"error": True, "value": "INVALID_REFRESH_TOKEN"}
        refresh_format = refresh.split('.')
        if len(refresh_format) != 3:
            return {"error": True, "value": "INVALID_REFRESH_TOKEN"}
        return {"error": False, "value": refresh}

    def validate(self, attrs):
        '''
        attrs: ordered dict. contains all parameter that client sent to here as a request.
        '''
        # extract expected fields
        refresh = attrs.get('refresh', None)
        # ----------------------------------------------------------------------------------
        # validate fields
        refresh = self._validate_refresh(refresh=refresh)
        # ---------------------------------------------------------------------------------
        # check error exist or not
        errors = list()
        if refresh.get('error'):
            errors.append(refresh.get('value'))
        # ----------------------------------------------------------------------------------
        # if error(s) exists, raise validationError
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        # ----------------------------------------------------------------------------------
        try:
            refresh = RefreshToken(refresh.get('value'))
        except:
            raise CustomException(error_summary='INVALID_OR_EXPIRED_REFRESH_TOKEN')
        token = {"access": str(refresh.access_token)}
        if SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS'):
            if SIMPLE_JWT.get('BLACKLIST_AFTER_ROTATION'):
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass
            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()
            token["refresh"] = str(refresh)
        data = generate_response(keyword='TOKEN_GENERATED')
        data['token'] = token
        return data
