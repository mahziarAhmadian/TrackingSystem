from django.db import models


class Ters(models.Model):
    name = models.CharField(max_length=250)
