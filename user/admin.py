from pyexpat import model
from statistics import mode
from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    fields = ('phone_number', 'password', 'registered_at', 'is_active',
              'is_staff', 'is_superuser', 'phone_number_is_valid', 'blocked', 'last_login', 'permissions', 'notes')


@admin.register(models.VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    fields = ('type', 'code', 'user', 'expired_at')
