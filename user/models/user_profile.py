import uuid
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    email_is_verified = models.BooleanField(default=False, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=200, null=True, blank=True)
    national_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    information = models.JSONField(null=True, blank=True)
    create_time = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    def __str__(self) -> str:
        return "{} {}".format(self.first_name, self.last_name)
