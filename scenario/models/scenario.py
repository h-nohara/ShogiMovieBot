from django.db import models

# db
from accounts.models.project import Project

class Scenario(models.Model):

    class Meta:
        db_table = "scenarios"

    project = models.ForeignKey(
        Project,
        related_name = 'scenarios',
        on_delete = models.SET_NULL,
        null = True
    )

    title = models.CharField(
        verbose_name = "title",
        max_length = 1000,
        null = True
    )

    thumb_path = models.CharField(
        verbose_name = "thumb_path",
        max_length = 1000,
        null = True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
