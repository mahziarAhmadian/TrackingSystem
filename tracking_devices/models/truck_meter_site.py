import uuid
from django.db import models
from django.utils import timezone
from .meter_site import MeterSite
from .truck import Truck


class TruckMeterSite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    information = models.JSONField()
    create_time = models.DateTimeField(default=timezone.now)
    meter_site = models.ForeignKey(MeterSite, on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self) -> str:
        return "{}".format(self.id)
