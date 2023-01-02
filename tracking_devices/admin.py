from django.contrib import admin
# Register your models here.
from . import models


@admin.register(models.Module)
class ModuleAdmin(admin.ModelAdmin):
    fields = ('name', 'serial_number', 'information', 'create_time',)


@admin.register(models.Meter)
class MeterAdmin(admin.ModelAdmin):
    fields = ('name', 'serial_number', 'information', 'module',)
