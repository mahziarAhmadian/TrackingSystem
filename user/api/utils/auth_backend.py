from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


class AuthenticationWithEmailORPhoneNumber(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        User = get_user_model()
        user = None
        try:
            user = User.objects.get(phone_number=username)
        except:
            try:
                user = User.objects.get(email=username)
            except:
                return
        password_is_valid = check_password(password, user.password)
        if password_is_valid:
            return user
        return

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return
