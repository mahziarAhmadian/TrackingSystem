from django.contrib import admin
# Register your models here.
from . import models


@admin.register(models.Module)
class ModuleAdmin(admin.ModelAdmin):
    fields = ('name', 'serial_number', 'information', 'create_time',)


@admin.register(models.Meter)
class MeterAdmin(admin.ModelAdmin):
    fields = ('name', 'serial_number', 'information', 'module',)


@admin.register(models.Truck)
class TruckAdmin(admin.ModelAdmin):
    fields = ('name', 'number_plate', 'model', 'information', 'meter', 'driver', 'owner',)


@admin.register(models.TruckingRecords)
class TruckRecordAdmin(admin.ModelAdmin):
    fields = ('lat', 'long', 'consumption', 'information', 'module', 'meter', 'truck',)


@admin.register(models.MeterType)
class MeterTypeAdmin(admin.ModelAdmin):
    fields = ('english_name', 'persian_name')
