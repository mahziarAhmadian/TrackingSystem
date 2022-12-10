import uuid
from django.db import models
from .project import Project
from django.utils import timezone


class ProjectDocument(models.Model):
    TYPE_CHOICES = (
        ('S', 'single'),
        ('M', 'municipality'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=80, choices=TYPE_CHOICES)
    link = models.URLField()
    information = models.JSONField()
    create_time = models.DateTimeField(default=timezone.now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "documents : {} for project {}-{} ".format(self.title, self.project.farsi_name,
                                                          self.project.english_name)
