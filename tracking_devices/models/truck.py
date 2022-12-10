import uuid
from django.db import models
from django.utils import timezone
from . import User
from .meter import Meter


class Truck(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    numberplate = models.CharField(max_length=255, unique=True)
    model = models.IntegerField()
    information = models.JSONField()
    create_time = models.DateTimeField(default=timezone.now)
    meter = models.OneToOneField(Meter, on_delete=models.CASCADE)
    driver = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_name')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_name')

    def __str__(self) -> str:
        return "{}".format(self.name)
