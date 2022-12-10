import uuid
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    email_is_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=200)
    national_id = models.CharField(max_length=10, unique=True)
    information = models.JSONField()
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return "{} {}".format(self.first_name, self.last_name)
