from django.db import models
from django.utils import timezone
from user.models import User


class VerificationCode(models.Model):
    TYPE_CHOICES = (
        ('E', 'email'),
        ('P', 'phone'),
        ('EN', 'entrance'),
        ('RST', 'resetPassword')
    )

    type = models.CharField(max_length=80, choices=TYPE_CHOICES)
    code = models.CharField(max_length=80)
    sent = models.BooleanField(default=False)
    expired_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{} verification code for {}: {}".format(
            self.type, self.user.phone_number, self.code)
