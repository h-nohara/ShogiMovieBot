from django.db import models

# db
from accounts.models.user import User

class Project(models.Model):

    class Meta:
        db_table = "projects"

    user = models.ForeignKey(
        User,
        related_name = 'projects',
        on_delete = models.SET_NULL,
        null = True
    )

    title = models.CharField(
        verbose_name = "title",
        max_length = 1000,
        null = True
    )

    pickle_basename = models.CharField(
        verbose_name = "pickle_path",
        max_length = 1000,
        null = True
    )


    pickle_path = models.CharField(
        verbose_name = "pickle_path",
        max_length = 1000,
        null = True
    )

    concat_movie_path = models.CharField(
        verbose_name = "concat_movie_path",
        max_length = 1000,
        null = True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    