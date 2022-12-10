import uuid
from django.db import models
from django.utils import timezone
from .module import Module
from .meter import Meter
from .truck import Truck


class TruckingRecords(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lat = models.FloatField()
    long = models.FloatField()
    consumption = models.FloatField()
    information = models.JSONField()
    create_time = models.DateTimeField(default=timezone.now)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{}".format(self.id)
