from pyexpat import model
from statistics import mode
from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    fields = ('phone_number', 'password', 'registered_at', 'is_active',
              'is_staff', 'is_superuser', 'phone_number_is_valid', 'blocked', 'last_login', 'permissions', 'notes',
              'profile', 'type')


@admin.register(models.VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    fields = ('type', 'code', 'user', 'expired_at')


@admin.register(models.UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('email', 'email_is_verified', 'first_name', 'last_name', 'zip_code', 'national_id', 'information')


@admin.register(models.UserImage)
class UserImageAdmin(admin.ModelAdmin):
    fields = ('user', 'sm_image', 'md_image', 'lg_image',)
