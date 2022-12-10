from email.policy import default
from enum import unique
from random import choices
from django.db import models


class Response(models.Model):
    STATUS_CHOICES = (
        ('S', 'success'),
        ('F', 'failed')
    )
    status = models.CharField(max_length=80, choices=STATUS_CHOICES)
    status_code = models.IntegerField(default=200)
    summary = models.CharField(max_length=120, unique=True)
    error_code = models.IntegerField()
    english_details = models.CharField(max_length=400)
    farsi_details = models.CharField(max_length=400)

    def __str__(self) -> str:
        return self.summary
