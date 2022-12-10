from rest_framework_simplejwt.authentication import JWTAuthentication
from core.settings import EXCLUDED_AUTHENTICATION_APIS
from .custom_exception import CustomException


class CustomJWTAuthentication(JWTAuthentication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self, request):
        try:
            auth_results = super().authenticate(request)
        except:
            raise CustomException(error_summary='UNAUTHORIZED_ACCESS')
        if auth_results is None:
            raise CustomException(error_summary='UNAUTHORIZED_ACCESS')
        return auth_results


def get_authetication_classes(api):
    if api in EXCLUDED_AUTHENTICATION_APIS:
        return []
    return [CustomJWTAuthentication]
