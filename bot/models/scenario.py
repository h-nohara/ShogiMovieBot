from django.db import models
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
        verbose_name = "title",
        max_length = 1000,
        null = True
    )

    is_public = models.BooleanField(
        verbose_name = "public or not",
        default = False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    