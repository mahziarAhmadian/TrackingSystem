from django.db import models
from django.utils import timezone


class Permission(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title

"""
    system permissions : 
    AddType , EditType , DeleteType , EditUser , GetUserDetail , DeleteUser , AddProject, EditProject , DeleteProject
"""