import uuid
from django.db import models
from django.utils import timezone
from .module import Module
from .meter_type import MeterType


class Meter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=250, unique=True)
    information = models.JSONField()
    create_time = models.DateTimeField(default=timezone.now)
    module = models.OneToOneField(Module, on_delete=models.CASCADE)
    meter_type = models.ForeignKey(MeterType, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self) -> str:
        return "{} - {} ".format(self.name, self.serial_number)
