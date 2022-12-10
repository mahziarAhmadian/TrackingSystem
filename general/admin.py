from django.contrib import admin
from . import models


@admin.register(models.Response)
class UserAdmin(admin.ModelAdmin):
    pass
