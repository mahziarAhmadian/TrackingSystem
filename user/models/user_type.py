import uuid
from django.db import models
from django.utils import timezone


class UserType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    english_name = models.CharField(max_length=255)
    persian_name = models.CharField(max_length=255)
    information = models.JSONField()
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return "{} {}".format(self.english_name, self.persian_name)
