from pyexpat import model
from statistics import mode
from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'phone_number', 'email', 'national_id', 'registered_at', 'is_active',
              'is_staff', 'is_superuser', 'email_is_valid', 'phone_number_is_valid', 'blocked', 'last_login')


@admin.register(models.VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    fields = ('type', 'code', 'user', 'expired_at')
