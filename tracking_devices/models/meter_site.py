import uuid
from django.db import models
from django.utils import timezone
from . import User


class TruckingRecords(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField()
    lat = models.FloatField()
    long = models.FloatField()
    information = models.JSONField()
    create_time = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{}".format(self.id)