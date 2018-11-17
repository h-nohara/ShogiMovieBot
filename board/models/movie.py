from django.db import models

# db
from accounts.models.project import Project

class Movie(models.Model):

    class Meta:
        db_table = "movies"

    project = models.ForeignKey(
        "accounts.Project",
        related_name = 'movies',
        on_delete = models.SET_NULL,
        null = True
    )

    basename = models.CharField(
        verbose_name = "basename",
        max_length = 1000,
        null = True
    )

    path = models.CharField(
        verbose_name = "path",
        max_length = 1000,
        null = True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
