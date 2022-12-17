import uuid

from django.db import models
from user.models import User
from django.utils import timezone


class UserImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    sm_image = models.ImageField(null=True, blank=True)
    md_image = models.ImageField(null=True, blank=True)
    lg_image = models.ImageField(null=True, blank=True)
    create_time = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    def __str__(self) -> str:
        return "image for user {}".format(self.user.phone_number)
