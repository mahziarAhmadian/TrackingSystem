import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from authorization.models import Permission
from general.utils.handle_exception import CustomException


class UserManager(BaseUserManager):
    """
    Custom user model manager.
    """

    def create_user(self, phone_number, password, **extra_fields):
        """
        Create and save a User with the given phone_number and password.
        """
        if not phone_number:
            raise CustomException(error_summary='PHONE_NUMBER_REQUIRED')
        if not password:
            raise CustomException(error_summary='PASSWORD_REQUIRED')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        try:
            user.save()
            return user
        except:
            raise CustomException(error_summary='USER_ALREADY_EXISTS')

    def create_superuser(self, phone_number, password, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone_number, password, **extra_fields)


# ---------------------------------------------------------------------------------------------


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='Email Address', blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    country_code = models.CharField(max_length=4, default="+98")
    phone_number = models.CharField(max_length=255, unique=True)
    email_is_valid = models.BooleanField(default=False)
    phone_number_is_valid = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    registered_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    notes = models.TextField(default="")
    national_id = models.CharField(max_length=12, default='', blank=True)

    permissions = models.ManyToManyField(Permission)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return "{} {} - {}".format(self.first_name, self.last_name, self.phone_number)
