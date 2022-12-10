import uuid

from django.db import models
from user.models import User
from django.utils import timezone


class UserImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sm_image = models.ImageField()
    md_image = models.ImageField()
    lg_image = models.ImageField()
    create_time = models.DateTimeField(timezone.now)

    def __str__(self) -> str:
        return "image for user {}".format(self.user.phone_number)
