import uuid

from django.db import models
from user.models import User
from django.utils import timezone


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    english_name = models.CharField(max_length=255)
    persian_name = models.CharField(max_length=255)
    image = models.ImageField(null=True)
    location = models.CharField(max_length=255)
    location_range = models.JSONField(null=True)
    started_from = models.DateTimeField()
    deadline = models.DateTimeField()
    contract_number = models.CharField(max_length=255)
    contract_information = models.JSONField(null=True)
    information = models.JSONField()
    create_time = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='onwer', null=True, blank=True)
    employer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='employer')

    def __str__(self) -> str:
        return "{} -- {}".format(self.english_name, self.id)
